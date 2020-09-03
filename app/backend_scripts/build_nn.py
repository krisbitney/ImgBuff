from fastai.vision import *
from fastai.vision.gan import *

# This module contains functions used to load the neural network from pytorch

# paths
parent = Path(__file__).parent
path_data = parent/'models'
color = 'color'
grayscale = 'grayscale'
colorized = 'colorized'
path_color = path_data/color
path_gray = path_data/grayscale
if not path_color.exists():
    path_color.mkdir(parents=True)
if not path_gray.exists():
    path_gray.mkdir(parents=True)


def get_generator_data(bs, size, p=1.):
    # data source
    label_func = lambda x : path_color/x.name
    src = (ImageImageList
           .from_folder(path_gray).use_partial_data(p)
           .split_none()
           .label_from_func(label_func))
    # data bunch
    data = src.transform(tfms=get_transforms(), size=size, tfm_y=True).databunch(bs=bs).normalize(imagenet_stats, do_y=True)
    data.c = 3
    return data


def get_critic_data(classes, bs, size):
    # data source
    src = (ImageList
           .from_folder(path_data, include=classes)
           .split_none()
           .label_from_folder(classes=classes))
    # data bunch
    data = src.transform(tfms=get_transforms(), size=size).databunch(bs=bs).normalize(imagenet_stats)
    data.c = 3
    return data


def get_generator(data_gen):
    wd = 1e-3
    arch = models.resnet34
    loss_gen = MSELossFlat()
    return unet_learner(data_gen, arch, loss_func=loss_gen,
                        wd=wd, blur=True, norm_type=NormType.Weight,
                        self_attention=True)


def get_critic(data_crit, metrics):
    wd = 1e-3
    loss_crit = AdaptiveLoss(nn.BCEWithLogitsLoss())
    return Learner(data_crit, gan_critic(), metrics=metrics,
                   loss_func=loss_crit, wd=wd)


def refresh_gan(version, crit_thresh=0.65, loss_weights=(1.,50.), bs=1, size=320, p=1.):
    wd = 1e-3
    data_gen = get_generator_data(bs, size, p)
    data_crit = get_critic_data([grayscale, color], bs=bs, size=size)
    generator = get_generator(data_gen)
    critic = get_critic(data_crit, metrics=None)
    switcher = partial(AdaptiveGANSwitcher, critic_thresh=crit_thresh)
    generator.path = parent.parent
    generator.model_dir = parent.parent
    if version == 'pre':
        generator.load('gen-pre')
        critic.load('critic-pre')
        return GANLearner.from_learners(generator, critic, weights_gen=loss_weights,
                                        show_img=True, switcher=switcher,
                                        opt_func=optim.Adam, wd=wd)
    gan = GANLearner.from_learners(generator, critic, weights_gen=loss_weights,
                                    show_img=True, switcher=switcher,
                                    opt_func=optim.Adam, wd=wd)
    gan.path = parent.parent
    gan.model_dir = parent.parent
    gan.load(version)
    return generator