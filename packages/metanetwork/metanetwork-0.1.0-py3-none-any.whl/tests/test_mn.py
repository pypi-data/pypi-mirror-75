import pytest

from .test_fixtures import bc_dataset, iris_dataset

from metanetwork import NeuralNetwork, MetaNetwork

train_X_bc, train_Y_bc, test_X_bc, test_Y_bc = bc_dataset()
train_X_iris, train_Y_iris, test_X_iris, test_Y_iris = iris_dataset()

def create_binary_network():
	e_binary = [NeuralNetwork(), NeuralNetwork(), NeuralNetwork(), NeuralNetwork()]
	for e in e_binary[:-1]:
		e.n_classes_ = 3
	e_binary[-1].n_classes_ =  2
	return [e_binary[:-1], e_binary[-1:]]

def create_multi_network():
	e_multi = [NeuralNetwork(), NeuralNetwork(), NeuralNetwork(), NeuralNetwork()]
	for e in e_multi[:-1]:
		e.n_classes_ = 2
	e_multi[-1].n_classes_ =  3
	return [e_multi[:-1], e_multi[-1:]]

@pytest.mark.parametrize("params", [
	({}),
	({'loss':'mse'})
])

class TestMetaNetwork:
	def test_mn_binary(self, params):
		network = create_binary_network()
		mn = MetaNetwork(network, **params)
		mn.fit(train_X_bc, train_Y_bc)

	def test_mn_multi(self, params):
		network = create_multi_network()
		mn = MetaNetwork(network, **params)
		mn.fit(train_X_iris, train_Y_iris)

	def test_mn_predict_binary(self, params):
		network = create_binary_network()
		mn = MetaNetwork(network, **params)
		mn.fit(train_X_bc, train_Y_bc)
		mn.predict(test_X_bc)

	def test_mn_predict_multi(self, params):
		network = create_multi_network()
		mn = MetaNetwork(network, **params)
		mn.fit(train_X_iris, train_Y_iris)
		mn.predict(test_X_iris)

def test_mn_unfit():
	network = create_binary_network()
	mn = MetaNetwork(network)
	with pytest.raises(RuntimeError):
		mn.predict(test_X_bc)

def test_mn_importance():
	network = create_multi_network()
	mn = MetaNetwork(network).fit(train_X_iris, train_Y_iris)
	mn.feature_importance(train_X_iris, train_Y_iris)
