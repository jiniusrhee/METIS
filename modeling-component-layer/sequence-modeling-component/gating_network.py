import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

class HGN(nn.Module):
    def __init__(self, num_users, num_items, args):
        
        super(HGN, self).__init__()
        self.args = args
        # init args
        L = args.sequence_length
        dims = args.dims

        # padding_idx =0.        
        self.U = nn.Embedding(num_users, dims)
        self.E = nn.Embedding(num_items, dims, padding_idx=0)

        self.feature_gate_item = nn.Linear(dims, dims)
        self.feature_gate_user = nn.Linear(dims, dims)

        self.instance_gate_item = Variable(torch.zeros(dims, 1).type(torch.FloatTensor), requires_grad=True).cuda()
        self.instance_gate_user = Variable(torch.zeros(dims, L).type(torch.FloatTensor), requires_grad=True).cuda()
   
        #
        self.instance_gate_item = torch.nn.init.xavier_uniform_(self.instance_gate_item)
        self.instance_gate_user = torch.nn.init.xavier_uniform_(self.instance_gate_user)

        self.Q = nn.Embedding(num_items, dims, padding_idx=0)
        self.Qb = nn.Embedding(num_items, 1, padding_idx=0)
        # weight initialization
        self.Q.weight.data.normal_(0, 1.0 / self.Q.embedding_dim)
