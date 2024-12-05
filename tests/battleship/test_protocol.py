import battleship	as B
import pytest

from battleship		import pb

@pytest.fixture
def examples():
	p = B.Protocol()

	res = pb.Response()
	res.token = 10
	res.type = pb.RsType.RS_HIT
	res.hit.CopyFrom(p.makeHit(B.BoardPoint(3, 5)))

	req = pb.Request()
	req.token = 10
	req.type = pb.RqType.RQ_HIT
	req.hit.CopyFrom(p.makeHit(B.BoardPoint(1, 4)))

	return {
		'raw-res':	res.SerializeToString(),
		'raw-req':	req.SerializeToString()
	}



class TestProtocol:
	def test_parseResponse(self, examples):
		p = B.Protocol()
		t = p.parseResponse(examples['raw-res'])

		assert type(t) is B.BoardPoint
		assert t.x == 3
		assert t.y == 5 

	def test_parseRequest(self, examples):
		p = B.Protocol()
		t = p.parseRequest(examples['raw-req'])

		assert type(t) is B.BoardPoint
		assert t.x == 1
		assert t.y == 4 

	def test_makeHitReq(self):
		p = B.Protocol()
		p.setToken(10)
		t = p.makeHitReq(B.BoardPoint(1, 5))
		assert type(t) is bytes

	def test_makeRegisterReq(self):
		p = B.Protocol()
		p.setToken(10)
		t = p.makeRegisterReq('test')
		assert type(t) is bytes
		
	def test_makeUpdateReq(self):
		p = B.Protocol()
		p.setToken(10)
		t = p.makeUpdateReq()
		assert type(t) is bytes
