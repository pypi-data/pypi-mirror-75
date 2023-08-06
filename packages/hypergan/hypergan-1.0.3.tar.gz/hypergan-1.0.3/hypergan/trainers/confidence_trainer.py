import numpy as np
import torch
import hyperchamber as hc
import inspect
from torch.autograd import Variable

from hypergan.trainers.alternating_trainer import AlternatingTrainer

class ConfidenceTrainer(AlternatingTrainer):
    """ Measures D confidence and steps when it stops changing """
    def _create(self):
        self.d_optimizer = self.create_optimizer("d_optimizer")
        self.g_optimizer = self.create_optimizer("g_optimizer")
        self.accumulated_g_grads = None
        self.accumulation_steps = 1
        self.max_grads = None
        self.min_grads = None
        self.relu = torch.nn.ReLU()


    def accumulate_g_grads(self):
        gs = self.g_grads()
        if self.accumulated_g_grads is None:
            self.accumulated_g_grads = [g.clone() for g in gs]
            self.max_grads = [g.clone() for g in gs]
            self.min_grads = [g.clone() for g in gs]
        else:
            for i, g in enumerate(self.accumulated_g_grads):
                self.max_grads[i] = torch.max(self.accumulated_g_grads[i], gs[i].clone())
                self.min_grads[i] = torch.min(self.accumulated_g_grads[i], gs[i].clone())
            self.accumulated_g_grads[i] += gs[i].clone()
            self.accumulation_steps += 1


    def calculate_d_gradients(self, x, g):
        self.d_optimizer.zero_grad()
        self.setup_gradient_flow(self.gan.d_parameters(), self.gan.g_parameters())
        D = self.gan.discriminator
        d_real = D(x)
        d_fake = D(g)

        d_loss, _ = self.gan.loss.forward(d_real, d_fake)#TODO targets=['d']
        self.gan.add_metric('d_loss', d_loss.mean())
        self.gan.x = x
        self.gan.d_fake = d_fake
        self.gan.d_real = d_real
        d_loss += sum([l[0] for l in self.train_hook_losses() if l[0] is not None])
        d_loss = d_loss.mean()

        return self.grads_for(d_loss, self.gan.d_parameters())

    def calculate_g_gradients(self):
        for i, g in enumerate(self.accumulated_g_grads):
            range_stddev = (self.max_grads[i]-self.min_grads[i])/4.0
            spread_ratio = (range_stddev / ((g/self.accumulation_steps)+1e-12)).abs()
            doubt = torch.clamp(self.relu((self.config.allowed_variance or 1.0) - spread_ratio/(self.config.max_spread or 0.2)), max=1.0)
            #if self.config.verbose:
            #    print("confidence >>", i, doubt.sum(), "/", np.prod(g.shape), "=", ("%d" % (doubt.sum()/np.prod(g.shape) * 100.0).item())+"%")
            self.accumulated_g_grads[i] = g/self.accumulation_steps * doubt
        g_grads = self.accumulated_g_grads
        self.accumulated_g_grads = None
        self.accumulation_steps = 1

        return g_grads

    def confidence(self):
        confidence = 0
        for i, g in enumerate(self.accumulated_g_grads):
            range_stddev = (self.max_grads[i]-self.min_grads[i])/4.0
            spread_ratio = (range_stddev / ((g/self.accumulation_steps)+1e-12)).abs()
            doubt = torch.clamp(self.relu((self.config.allowed_variance or 1.0) - spread_ratio/(self.config.max_spread or 0.2)), max=1.0)
            confidence += np.prod(g.shape) - doubt.sum()
            #if self.config.verbose:
            #    print("confidence >>", i, doubt.sum(), "/", np.prod(g.shape), "=", ("%d" % (doubt.sum()/np.prod(g.shape) * 100.0).item())+"%")
        return confidence


    def _step(self, feed_dict):
        metrics = self.gan.metrics()

        self.before_step(self.current_step, feed_dict)

        self.x = self.gan.inputs.next()
        g = self.gan.generator(self.gan.latent.next())
        confidence_loss = 1e10 + torch.zeros([1])
        confidence = 1e10 + torch.zeros([1])
        i=0
        self.accumulate_g_grads()
        d_grads = self.calculate_d_gradients(self.x, g)
        self.train_d(d_grads)

        while confidence_loss.abs() > (self.config.threshold or 1000):
            i+= 1
            if self.config.max_steps and i > self.config.max_steps:
                break
            self.accumulate_g_grads()
            d_grads = self.calculate_d_gradients(self.x, g)
            new_confidence = self.confidence()
            confidence_loss = confidence - new_confidence
            confidence = new_confidence
            if self.config.verbose:
                print("Confidence:", i, confidence.item(), confidence_loss.item())
            self.train_d(d_grads)
        print(i, "d steps")
        g_grads = self.calculate_g_gradients()
        self.train_g(g_grads)

        self.after_step(self.current_step, feed_dict)

        if self.current_step % 20 == 0:
            self.print_metrics(self.current_step)


