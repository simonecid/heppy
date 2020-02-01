class TriggerObject(object):

  '''Naive particle with pt, eta, phi and pdgid'''  
  def __init__(self, *args, **kwargs):
    self._pt = kwargs.get('pt', 0)
    self._eta = kwargs.get('eta', 0)
    self._phi = kwargs.get('phi', 0)
    self._pdgid = kwargs.get('pdgid', 0)
  # End __init__

  def pt(self):
    return self._pt
  # End pt
  
  def phi(self):
    return self._phi
  # End phi
  
  def eta(self):
    return self._eta
  # End eta

  def pdgid(self):
    return self._pdgid
  # End pdgid

# End class