import os
import tensorflow as tf
import datetime as dt
import csv
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, serializers, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from backend.quickstart.serializers import UserSerializer, GroupSerializer
import tensorflow as tf
from model.lib import data_utils
from model.lib.seq2seq_model_utils import create_model, get_predicted_sentence
from model.lib.chat import sentence_split, sentence_combine

class arg():
  batch_size = 1
  vocab_size = 300000
  size = 512
  num_layers = 4
  beam_size = 1   # int
  antilm = 0.0    # float
  n_bonus = 0.0
  gpu_usage = 1.0    # float
  buckets = [(5, 10), (10, 15), (20, 25), (40, 50)]
  max_gradient_norm = 5.0
  max_train_data_size = 0
  learning_rate = 0.5
  learning_rate_decay_factor = 0.99
  steps_per_checkpoint = 500
  en_tfboard = False
  workspace = 'model/works/mion'
  model_dir = '%s/nn_models' % workspace
  data_dir = '%s/data' % workspace

class Model():
  def __init__(self):
    os.environ['CUDA_VISIBLE_DEVICES'] = ''  # cpu is enough
    self.args = arg()
    self.sess = tf.Session()
    self.model = create_model(self.sess, self.args)
    self.vocab, self.rev_vocab = data_utils.initialize_vocabulary(os.path.join(self.args.data_dir, 'vocab300000.in'))
     
  def predict(self, sentence):
    if len(sentence.split(' ')) < 2:
      sentence = sentence_split(sentence)

    predicted_sentence = get_predicted_sentence(self.args, sentence, self.vocab, self.rev_vocab, self.model, self.sess)
    if isinstance(predicted_sentence, list):
      ret = ''
      for sent in predicted_sentence:
        ret += sentence_combine(sent['dec_inp'])
    else:
      ret = predicted_sentence
    
    return ret
  
modelSingleton = Model()

class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  queryset = User.objects.all().order_by('-date_joined')
  serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows groups to be viewed or edited.
  """
  queryset = Group.objects.all()
  serializer_class = GroupSerializer

def getIP(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def chat(request):
  msg = request.GET.get('msg', '')

  with open('history.csv', 'a') as file:
    w = csv.writer(file)
    w.writerow([msg, getIP(request), dt.datetime.now()])

  return Response({'message': modelSingleton.predict(msg)})
