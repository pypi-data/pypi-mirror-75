# AUTOGENERATED! DO NOT EDIT! File to edit: utils.ipynb (unless otherwise specified).

__all__ = ['args_loop', 'Converter', 'Torch2np', 'torch2np', 'Np2torch', 'np2torch', 'numpyify', 'assert_allclose',
           'assert_allclose_f', 'assert_allclose_f_ttn', 'reverse', 'shape', 'stackify', 'delete', 'rescale',
           'singlify', 'augment', 'deaugment', 'normalize', 'ps_bb', 'array_bb', 'bb_sz', 'bb_grid', 'bb_array',
           'is_p_in_bb', 'is_bb_in_bb', 'is_p_in_b', 'grid2ps', 'array_ps', 'crrgrid', 'csrgrid', 'csdgrid', 'cfpgrid',
           'unitize', 'cross_mat', 'pmm', 'condition_mat', 'condition', 'homography', 'approx_R', 'euler2R', 'R2euler',
           'rodrigues2R', 'R2rodrigues', 'approx_R', 'Rt2M', 'M2Rt', 'invert_rigid', 'mult_rigid', 'random_unit',
           'v_v_angle', 'v_v_R', 'pm2l', 'ps2l', 'pld', 'l_l_intersect', 'bb_ls', 'bb_l_intersect', 'sample_2pi',
           'sample_ellipse', 'ellipse2conic', 'conic2ellipse', 'rgb2gray', 'imresize', 'conv2d', 'pad', 'grad_array',
           'interp_array', 'wlstsq', 'get_colors', 'get_notebook_file', 'save_notebook', 'build_notebook',
           'convert_notebook']

# Cell
import hashlib
import json
import math
import os
import re
import time
import warnings
from pathlib import Path

import ipykernel
import nbdev.export
import numpy as np
import requests
import seaborn as sns
import torch
from IPython.display import Javascript, display
from notebook.notebookapp import list_running_servers
from PIL import Image
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from torchvision import transforms

# Cell
def args_loop(args, callback):
    if isinstance(args, tuple):  return tuple([args_loop(arg, callback) for arg in args])
    elif isinstance(args, dict): return {key: args_loop(arg, callback) for key,arg in args.items()}
    else:                        return callback(args)

# Cell
class Converter():
    def __init__(self): self.converted = False

    def predicate(self, arg): raise NotImplementedError('Please implement predicate')
    def formatter(self, arg): raise NotImplementedError('Please implement formatter')

    def callback(self, arg):
        if self.predicate(arg):
            self.converted = True
            return self.formatter(arg)
        else:
            return arg

    def __call__(self, args):
        self.converted = False
        return args_loop(args, self.callback)

# Cell
class Torch2np(Converter):
    def predicate(self, arg): return isinstance(arg, torch.Tensor)
    def formatter(self, arg): return arg.detach().cpu().numpy()
torch2np = Torch2np()

# Cell
class Np2torch(Converter):
    def predicate(self, arg): return isinstance(arg, np.ndarray)
    def formatter(self, arg): return torch.from_numpy(arg)
np2torch = Np2torch()

# Cell
def numpyify(f):
    def _numpyify(*args, **kwargs):
        np2torch = Np2torch() # For thread safety, make a local copy
        args, kwargs = np2torch((args, kwargs))
        out = f(*args, **kwargs)
        if np2torch.converted: out = torch2np(out)
        return out
    return _numpyify

# Cell
def _assert_allclose(A, B, **kwargs):
    if isinstance(A, tuple):
        for a,b in zip(A,B): _assert_allclose(a, b, **kwargs)
    elif isinstance(A, dict):
        for key in A.keys() & B.keys(): _assert_allclose(A[key], B[key], **kwargs)
    else:
        try:    assert(np.allclose(A, B, **kwargs))
        except: assert(np.all(A == B))

# Cell
def assert_allclose(A, B, **kwargs): _assert_allclose(*torch2np((A, B)), **kwargs)

# Cell
def assert_allclose_f(f, x, y, **kwargs):
    if not isinstance(x, tuple): x = (x,)
    assert_allclose(f(*x), y, **kwargs)

# Cell
def assert_allclose_f_ttn(f, x, y, **kwargs): # ttn == "torch, then numpy"
    torch2np = Torch2np()
    assert_allclose_f(f, x, y, **kwargs) # Torch test
    x, y = torch2np((x, y))
    assert(torch2np.converted)           # Make sure something was converted
    assert_allclose_f(f, x, y, **kwargs) # Numpy test

# Cell
def reverse(A): return A[::-1]

# Cell
@numpyify
def shape(A, dtype=None):
    if dtype is None: dtype = A.dtype
    return A.new_tensor(A.shape, dtype=dtype)

# Cell
@numpyify
def stackify(A, dim=0):
    if isinstance(A, tuple): return torch.stack([stackify(a, dim) for a in A], dim)
    return A

# Cell
def delete(A, idx_delete):
    idx = torch.ones(len(A), dtype=torch.bool)
    idx[idx_delete] = False
    return A[idx]

# Cell
def rescale(A, r1, r2):
    return (A-r1[0])/(r1[1]-r1[0])*(r2[1]-r2[0])+r2[0]

# Cell
def singlify(f):
    def _singlify(ps, *args, **kwargs):
        single = len(ps.shape) == 1
        if single: ps = ps[None]
        ps = f(ps, *args, **kwargs)
        if single: ps = ps[0]
        return ps
    return _singlify

# Cell
@numpyify
@singlify
def augment(ps): return torch.cat([ps, ps.new_ones((len(ps), 1))], dim=1)

# Cell
@singlify
def deaugment(ps): return ps[:, 0:-1]

# Cell
@singlify
def normalize(ps): return deaugment(ps/ps[:, [-1]])

# Cell
@numpyify
def ps_bb(ps): return stackify((torch.min(ps, dim=0).values, torch.max(ps, dim=0).values))

# Cell
@numpyify
def array_bb(arr): return torch.LongTensor([[0,0], [arr.shape[1]-1, arr.shape[0]-1]])

# Cell
@numpyify
def bb_sz(bb): return torch.LongTensor([bb[1,1]-bb[0,1]+1, bb[1,0]-bb[0,0]+1])

# Cell
@numpyify
def bb_grid(bb, dtype):
    return stackify(reverse(torch.meshgrid(torch.arange(bb[0,1],bb[1,1]+1, dtype=dtype),
                                           torch.arange(bb[0,0],bb[1,0]+1, dtype=dtype))))

# Cell
def bb_array(arr, bb): return arr[bb[0,1]:bb[1,1]+1, bb[0,0]:bb[1,0]+1]

# Cell
def is_p_in_bb(p, bb): return p[0] >= bb[0,0] and p[1] >= bb[0,1] and p[0] <= bb[1,0] and p[1] <= bb[1,1]

# Cell
def is_bb_in_bb(bb1, bb2): return is_p_in_bb(bb1[0], bb2) and is_p_in_bb(bb1[1], bb2)

# Cell
def is_p_in_b(p, b): return Polygon(b).contains(Point(*p))

# Cell
@numpyify
def grid2ps(X, Y, order='row'):
    if   order == 'row': return stackify((X.flatten(), Y.flatten()), dim=1)
    elif order == 'col': return grid2ps(X.T, Y.T, order='row')
    else: raise RuntimeError(f'Unrecognized option: {order}')

# Cell
@numpyify
def array_ps(arr, dtype=None):
    if dtype is None: dtype = arr.dtype
    return grid2ps(*bb_grid(array_bb(arr), dtype))

# Cell
@numpyify
def crrgrid(p):
    num_h, num_w, spacing_h, spacing_w = p
    h, w = spacing_h*(num_h-1), spacing_w*(num_w-1)
    return grid2ps(*reverse(torch.meshgrid(torch.linspace(-h/2, h/2, int(num_h), dtype=p.dtype),
                                           torch.linspace(-w/2, w/2, int(num_w), dtype=p.dtype))),
                   'col')

# Cell
@numpyify
def csrgrid(p):
    num_h, num_w, spacing = p
    return crrgrid(stackify((num_h, num_w, spacing, spacing)))

# Cell
@numpyify
def csdgrid(p): # Pretty sure this implementation can be vastly improved
    num_h, num_w, spacing, fo = p
    h, w = spacing*(num_h-1), spacing*(num_w-1)
    xs_grid = torch.linspace(-w/2, w/2, int(num_w))
    ys_grid = torch.linspace(-h/2, h/2, int(num_h))
    ps = []
    for x_grid in xs_grid:
        if fo: ys, fo = ys_grid[0::2], False
        else:  ys, fo = ys_grid[1::2], True
        xs = x_grid.new_full((len(ys),), x_grid)
        ps.append(stackify((xs, ys), dim=1))
    return torch.cat(ps)

# Cell
@numpyify
def cfpgrid(p):
    two = p.new_tensor(2)
    h, w = p
    return crrgrid(stackify((two, two, h, w)))

# Cell
@singlify
@numpyify
def unitize(vs): return vs/torch.norm(vs, dim=1, keepdim=True)

# Cell
@numpyify
def cross_mat(v):
    zero = v.new_tensor(0)
    return stackify((( zero, -v[2],  v[1]),
                     ( v[2],  zero, -v[0]),
                     (-v[1],  v[0],  zero)))

# Cell
@singlify
def pmm(ps, A, aug=False):
    if aug: ps = augment(ps)
    ps = (A@ps.T).T
    if aug: ps = normalize(ps) # works for both affine and homography transforms
    return ps

# Cell
@numpyify
def condition_mat(ps):
    zero, one = ps.new_tensor(0), ps.new_tensor(1)

    xs, ys = ps[:, 0], ps[:, 1]
    mean_x, mean_y = xs.mean(), ys.mean()
    s_m = math.sqrt(2)*len(ps)/(torch.sqrt((xs-mean_x)**2+(ys-mean_y)**2)).sum()
    return stackify((( s_m, zero, -mean_x*s_m),
                     (zero,  s_m, -mean_y*s_m),
                     (zero, zero,         one)))

# Cell
def condition(ps):
    T = condition_mat(ps)
    return pmm(ps, T, aug=True), T

# Cell
@numpyify
def homography(ps1, ps2):
    # Condition and augment points
    (ps1_cond, T1), (ps2_cond, T2) = map(condition, [ps1, ps2])
    ps1_cond, ps2_cond = map(augment, [ps1_cond, ps2_cond])

    # Form homogeneous system
    L = torch.cat([torch.cat([ps1_cond, torch.zeros_like(ps1_cond), -ps2_cond[:, 0:1]*ps1_cond], dim=1),
                   torch.cat([torch.zeros_like(ps1_cond), ps1_cond, -ps2_cond[:, 1:2]*ps1_cond], dim=1)])

    # Solution is the last column of V
    H12_cond = torch.svd(L, some=False).V[:,-1].reshape(3,3)

    # Undo conditioning
    H12 = torch.inverse(T2)@H12_cond@T1
    H12 = H12/H12[2,2] # Sets H12[2,2] to 1
    return H12

# Cell
@numpyify
def approx_R(R):
    [U,_,V] = torch.svd(R)
    R = U@V.T
    if not torch.isclose(torch.det(R), R.new_tensor(1)):
        R = R.new_full((3,3), math.nan)
    return R

# Cell
@numpyify
def euler2R(euler):
    s, c = torch.sin, torch.cos
    e_x, e_y, e_z = euler
    return stackify((
        (c(e_y)*c(e_z), c(e_z)*s(e_x)*s(e_y) - c(e_x)*s(e_z), s(e_x)*s(e_z) + c(e_x)*c(e_z)*s(e_y)),
        (c(e_y)*s(e_z), c(e_x)*c(e_z) + s(e_x)*s(e_y)*s(e_z), c(e_x)*s(e_y)*s(e_z) - c(e_z)*s(e_x)),
        (      -s(e_y),                        c(e_y)*s(e_x),                        c(e_x)*c(e_y))
    ))

# Cell
@numpyify
def R2euler(R):
    return stackify((torch.atan2( R[2, 1], R[2, 2]),
                     torch.atan2(-R[2, 0], torch.sqrt(R[0, 0]**2+R[1, 0]**2)),
                     torch.atan2( R[1, 0], R[0, 0])))

# Cell
@numpyify
def rodrigues2R(r):
    zero = r.new_tensor(0)

    theta = torch.norm(r)
    if theta > math.pi: warnings.warn('Theta greater than pi')
    if torch.isclose(theta, zero): return torch.eye(3, dtype=r.dtype)
    u = r/theta
    return torch.eye(3, dtype=r.dtype)*torch.cos(theta) + \
           (1-torch.cos(theta))*u[:,None]@u[:,None].T + \
           cross_mat(u)*torch.sin(theta)

# Cell
@numpyify
def R2rodrigues(R):
    zero, one, pi = R.new_tensor(0), R.new_tensor(1), R.new_tensor(math.pi)

    A = (R-R.T)/2
    rho = A[[2,0,1],[1,2,0]]
    s = torch.norm(rho)
    c = (R.trace()-1)/2
    if torch.isclose(s, zero) and torch.isclose(c, one):
        r = R.new_zeros(3)
    elif torch.isclose(s, zero) and torch.isclose(c, -one):
        V = R + torch.eye(3, dtype=R.dtype)
        v = V[:, torch.where(~torch.isclose(torch.norm(V, dim=0), zero))[0][0]] # Just get first non-zero
        u = unitize(v)
        def S_half(r):
            if torch.isclose(torch.norm(r), pi) and \
               ((torch.isclose(r[0], zero) and torch.isclose(r[1], zero) and r[2] < 0) or \
                (torch.isclose(r[0], zero) and r[1] < 0) or \
                (r[0] < 0)):
                return -r
            else:
                return r
        r = S_half(u*math.pi)
    elif not torch.isclose(s, zero):
        u = rho/s
        theta = torch.atan2(s,c)
        r = u*theta
    else: raise RuntimeError('This shouldnt happen; please debug')
    return r

# Cell
@numpyify
def approx_R(R):
    [U,_,V] = torch.svd(R)
    R = U@V.T
    if not torch.isclose(torch.det(R), R.new_tensor(1)):
        R = R.new_full((3,3), math.nan)
    return R

# Cell
@numpyify
def Rt2M(R, t):
    assert_allclose(R.dtype, t.dtype)
    M = torch.cat([R, t[:,None]], dim=1)
    M = torch.cat([M, M.new_tensor([[0,0,0,1]])])
    return M

# Cell
def M2Rt(M): return M[0:3,0:3], M[0:3,3]

# Cell
def invert_rigid(M):
    R, t = M2Rt(M)
    return Rt2M(R.T, -R.T@t)

# Cell
def mult_rigid(M1, M2):
    assert_allclose(M1.dtype, M2.dtype)
    R1, t1 = M2Rt(M1)
    R2, t2 = M2Rt(M2)
    return Rt2M(R1@R2, R1@t2+t1)

# Cell
def random_unit(dtype):
    r = torch.ones(1, dtype=dtype)
    theta = torch.acos(rescale(torch.rand(1, dtype=dtype), [0,1], [-1,1]))
    phi = rescale(torch.rand(1, dtype=dtype), [0,1], [0, 2*math.pi])
    return spherical2cart(torch.cat((r, theta, phi)))

# Cell
@numpyify
def v_v_angle(a, b): return torch.acos(torch.dot(a,b)/(torch.norm(a)*torch.norm(b)))

# Cell
@numpyify
def v_v_R(v1, v2):
    zero = v1.new_tensor(0)

    theta = v_v_angle(v1, v2)
    v3 = torch.cross(v1, v2)
    if not torch.isclose(torch.norm(v3), zero): v3 = unitize(v3)
    return rodrigues2R(theta*v3)

# Cell
@numpyify
def pm2l(p, m):
    zero, one = p.new_tensor(0), p.new_tensor(1)

    x, y = p
    if not torch.isfinite(m): a, b, c = one, zero,    -x
    else:                     a, b, c =   m, -one, y-m*x
    return stackify((a,b,c))

# Cell
@numpyify
def ps2l(p1, p2):
    zero = p1.new_tensor(0)

    x1, y1 = p1
    x2, y2 = p2
    if not torch.isclose(x2-x1, zero): m = (y2-y1)/(x2-x1)
    else:                              m = p1.new_tensor(math.inf)
    return pm2l(p1, m)

# Cell
@numpyify
def pld(p, l):
    x, y = p
    a, b, c = l
    return torch.abs(a*x + b*y + c)/torch.sqrt(a**2 + b**2)

# Cell
@numpyify
def l_l_intersect(l1, l2):
    a1, b1, c1 = l1
    a2, b2, c2 = l2
    return stackify(((-c1*b2 + b1*c2)/(a1*b2 - b1*a2), (-a1*c2 + c1*a2)/(a1*b2 - b1*a2)))

# Cell
@numpyify
def bb_ls(bb, dtype):
    bb = bb.type(dtype)
    return stackify((ps2l(bb[[0,0],[0,1]], bb[[0,1],[0,1]]),
                     ps2l(bb[[0,0],[0,1]], bb[[1,0],[0,1]]),
                     ps2l(bb[[0,1],[0,1]], bb[[1,1],[0,1]]),
                     ps2l(bb[[1,0],[0,1]], bb[[1,1],[0,1]])))

# Cell
@numpyify
def bb_l_intersect(bb, l):
    bb = bb.type(l.dtype) # due to torch.isclose not working between different dtypes
    ls_bb = bb_ls(bb, l.dtype)
    ps = []
    for l_bb in ls_bb:
        p = l_l_intersect(l_bb, l)
        if (torch.isclose(p[0], bb[0,0]) or p[0] > bb[0,0]) and \
           (torch.isclose(p[0], bb[1,0]) or p[0] < bb[1,0]) and \
           (torch.isclose(p[1], bb[0,1]) or p[1] > bb[0,1]) and \
           (torch.isclose(p[1], bb[1,1]) or p[1] < bb[1,1]):
            ps.append(p)
    ps = tuple(ps)
    # TODO: handle edge cases (i.e. if line intersects corner or is colinear with edge)
    return stackify(ps)

# Cell
@numpyify
def sample_2pi(num_samples): return torch.linspace(0, 2*math.pi, int(num_samples)+1)[:-1]

# Cell
@numpyify
def sample_ellipse(e, num_samples):
    h, k, a, b, alpha = e
    thetas = sample_2pi(num_samples)
    return stackify((a*torch.cos(alpha)*torch.cos(thetas) - b*torch.sin(alpha)*torch.sin(thetas) + h,
                     a*torch.sin(alpha)*torch.cos(thetas) + b*torch.cos(alpha)*torch.sin(thetas) + k), dim=1)

# Cell
@numpyify
def ellipse2conic(e):
    h, k, a, b, alpha = e
    A = a**2*torch.sin(alpha)**2 + b**2*torch.cos(alpha)**2
    B = 2*(b**2 - a**2)*torch.sin(alpha)*torch.cos(alpha)
    C = a**2*torch.cos(alpha)**2 + b**2*torch.sin(alpha)**2
    D = -2*A*h - B*k
    E = -B*h - 2*C*k
    F = A*h**2 + B*h*k + C*k**2 - a**2*b**2
    return stackify(((  A, B/2, D/2),
                     (B/2,   C, E/2),
                     (D/2, E/2,   F)))

# Cell
@numpyify
def conic2ellipse(Aq):
    zero, pi = Aq.new_tensor(0), Aq.new_tensor(math.pi)

    A = Aq[0, 0]
    B = 2*Aq[0, 1]
    C = Aq[1, 1]
    D = 2*Aq[0, 2]
    E = 2*Aq[1, 2]
    F = Aq[2, 2]

    # Return nans if input conic is not ellipse
    if torch.any(~torch.isfinite(Aq)) or torch.isclose(B**2-4*A*C, zero) or B**2-4*A*C > 0:
        return Aq.new_full((5,), math.nan)

    # Equations below are from https://math.stackexchange.com/a/820896/39581

    # "coefficient of normalizing factor"
    q = 64*(F*(4*A*C-B**2)-A*E**2+B*D*E-C*D**2)/(4*A*C-B**2)**2

    # distance between center and focal point
    s = 1/4*torch.sqrt(torch.abs(q)*torch.sqrt(B**2+(A-C)**2))

    # ellipse parameters
    h = (B*E-2*C*D)/(4*A*C-B**2)
    k = (B*D-2*A*E)/(4*A*C-B**2)
    a = 1/8*torch.sqrt(2*torch.abs(q)*torch.sqrt(B**2+(A-C)**2)-2*q*(A+C))
    b = torch.sqrt(a**2-s**2)
    # Get alpha; note that range of alpha is [0, pi)
    if torch.isclose(q*A-q*C, zero) and torch.isclose(q*B, zero): alpha = zero # Circle
    elif torch.isclose(q*A-q*C, zero) and q*B > 0:                alpha = 1/4*pi
    elif torch.isclose(q*A-q*C, zero) and q*B < 0:                alpha = 3/4*pi
    elif q*A-q*C > 0 and (torch.isclose(q*B, zero) or q*B > 0):   alpha = 1/2*torch.atan(B/(A-C))
    elif q*A-q*C > 0 and q*B < 0:                                 alpha = 1/2*torch.atan(B/(A-C)) + pi
    elif q*A-q*C < 0:                                             alpha = 1/2*torch.atan(B/(A-C)) + 1/2*pi
    else: raise RuntimeError('"Impossible" condition reached; please debug')

    return stackify((h, k, a, b, alpha))

# Cell
def rgb2gray(arr): # From Pillow documentation
    return arr[:,:,0]*(299/1000) + arr[:,:,1]*(587/1000) + arr[:,:,2]*(114/1000)

# Cell
@numpyify
def imresize(arr, sz, mode='bilinear', align_corners=True):
    if not isinstance(sz, tuple): sz = tuple((shape(arr)//(shape(arr)/sz).min()).long())
    return torch.nn.functional.interpolate(arr[None, None, :, :],
                                           size=sz,
                                           mode=mode,
                                           align_corners=align_corners).squeeze(0).squeeze(0)

# Cell
@numpyify
def conv2d(arr, kernel, **kwargs):
    return torch.nn.functional.conv2d(arr[None,None], kernel[None, None], **kwargs).squeeze(0).squeeze(0)

# Cell
@numpyify
def pad(arr, pad, mode):
    return torch.nn.functional.pad(arr[None,None], pad, mode=mode).squeeze(0).squeeze(0)

# Cell
@numpyify
def grad_array(arr):
    kernel_sobel = arr.new_tensor([[-0.1250, 0, 0.1250],
                                   [-0.2500, 0, 0.2500],
                                   [-0.1250, 0, 0.1250]])
    arr = pad(arr, pad=(1,1,1,1), mode='replicate')
    return tuple(conv2d(arr, kernel) for kernel in (kernel_sobel, kernel_sobel.T))

# Cell
@numpyify
def interp_array(arr, ps, align_corners=True, **kwargs):
    # ps must be rescaled to [-1,1]
    ps = stackify((rescale(ps[:, 0], [0, arr.shape[1]-1], [-1, 1]),
                   rescale(ps[:, 1], [0, arr.shape[0]-1], [-1, 1])), dim=1)
    return torch.nn.functional.grid_sample(arr[None, None],
                                           ps[None, None],
                                           align_corners=align_corners,
                                           **kwargs).squeeze()

# Cell
@numpyify
def wlstsq(A, b, W=None):
    single = len(b.shape) == 1
    if single: b = b[:, None]
    if W is not None: # Weight matrix is a diagonal matrix with sqrt of the input weights
        W = torch.sqrt(W.reshape(-1,1))
        A, b = A*W, b*W
    x = torch.lstsq(b, A).solution[:A.shape[1],:] # first n rows contains solution
    if single: x = x.squeeze(1)
    return x

# Cell
def get_colors(n): return sns.color_palette(None, n)

# Cell
def get_notebook_file():
    id_kernel = re.search('kernel-(.*).json', ipykernel.connect.get_connection_file()).group(1)
    for server in list_running_servers():
        response = requests.get(requests.compat.urljoin(server['url'], 'api/sessions'),
                                params={'token': server.get('token', '')})
        for r in json.loads(response.text):
            if 'kernel' in r and r['kernel']['id'] == id_kernel:
                return Path(r['notebook']['path'])

# Cell
def save_notebook():
    file_notebook = get_notebook_file()
    _get_md5 = lambda : hashlib.md5(file_notebook.read_bytes()).hexdigest()
    md5_start = _get_md5()
    display(Javascript('IPython.notebook.save_checkpoint();')) # Asynchronous
    while md5_start == _get_md5(): time.sleep(1e-1)

# Cell
def build_notebook(save=True):
    if save: save_notebook()
    nbdev.export.notebook2script(fname=get_notebook_file().as_posix())

# Cell
def convert_notebook(save=True, t='markdown'):
    if save: save_notebook()
    os.system(f'jupyter nbconvert --to {t} {get_notebook_file().as_posix()}')