import torch
from math import sqrt as sqrt
from itertools import product as product


class PriorBox(object):
    """Compute prior box coordinates in center-offset form for each source
    feature map.
    Note:
    This 'layer' has changed between versions of the original SSD
    paper, so we include both versions, but note v2 is the most tested and most
    recent version of the paper.
    """
    def __init__(self, cfg):
        super(PriorBox, self).__init__()
        # self.image_size = cfg['image_size']
        self.variance = cfg['variance'] or [0.1]
        self.feature_maps = cfg['feature_maps']
        self.min_scale = cfg['min_scale']
        self.max_scale = cfg['max_scale']
        # self.steps = cfg['steps']
        self.aspect_ratios = cfg['aspect_ratios']
        self.clip = cfg['clip']
        self.version = cfg['name']
        for v in self.variance:
            if v <= 0:
                raise ValueError('Variances must be greater than 0')

        self.num_feat = len(self.feature_maps)
        s_k = list()
        for i in range(self.num_feat):
            s_k.append(self.min_scale +
                       (self.max_scale - self.min_scale)/(self.num_feat-1) * i)
        self.s_k = s_k

    def forward(self):
        mean = []
        # TODO merge these
        if self.version == 'v2':
            for k, f in enumerate(self.feature_maps):
                for i, j in product(range(f), repeat=2):

                    f_k = f
                    # f_k = self.image_size / self.steps[k]
                    # unit center x,y
                    cx = (j + 0.5) / f_k
                    cy = (i + 0.5) / f_k

                    # aspect_ratio: 1
                    # s_k = self.min_sizes[k]/self.image_size
                    s_k = self.s_k[k]
                    mean += [cx, cy, s_k, s_k]

                    # aspect_ratio: 1
                    # s_k_prime = sqrt(s_k * (self.max_sizes[k]/self.image_size))
                    if k == self.num_feat - 1:
                        s_k_prime = 1.0
                    else:
                        s_k_prime = self.s_k[k+1]
                    mean += [cx, cy, s_k_prime, s_k_prime]

                    # rest of aspect ratios
                    for ar in self.aspect_ratios[k]:
                        mean += [cx, cy, s_k*sqrt(ar), s_k/sqrt(ar)]
                        mean += [cx, cy, s_k/sqrt(ar), s_k*sqrt(ar)]

        else:
            # original version generation of prior (default) boxes
            for i, k in enumerate(self.feature_maps):
                step_x = step_y = self.image_size/k
                for h, w in product(range(k), repeat=2):
                    c_x = ((w+0.5) * step_x)
                    c_y = ((h+0.5) * step_y)
                    c_w = c_h = self.min_sizes[i] / 2
                    s_k = self.image_size  # 300
                    # aspect_ratio: 1,
                    # size: min_size
                    mean += [(c_x-c_w)/s_k, (c_y-c_h)/s_k,
                             (c_x+c_w)/s_k, (c_y+c_h)/s_k]
                    if self.max_sizes[i] > 0:
                        # aspect_ratio: 1
                        # size: sqrt(min_size * max_size)/2
                        c_w = c_h = sqrt(self.min_sizes[i] *
                                         self.max_sizes[i])/2
                        mean += [(c_x-c_w)/s_k, (c_y-c_h)/s_k,
                                 (c_x+c_w)/s_k, (c_y+c_h)/s_k]
                    # rest of prior boxes
                    for ar in self.aspect_ratios[i]:
                        if not (abs(ar-1) < 1e-6):
                            c_w = self.min_sizes[i] * sqrt(ar)/2
                            c_h = self.min_sizes[i] / sqrt(ar)/2
                            mean += [(c_x-c_w)/s_k, (c_y-c_h)/s_k,
                                     (c_x+c_w)/s_k, (c_y+c_h)/s_k]
        # back to torch land
        output = torch.Tensor(mean).view(-1, 4)
        if self.clip:
            output.clamp_(max=1, min=0)
        return output
