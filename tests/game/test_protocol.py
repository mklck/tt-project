import pytest

from game	import protobuf as pb, BoardPoint, Protocol

@pytest.fixture
def examples():
	p = Protocol()

	res = pb.Response()
	res.token = 10
	res.type = pb.RsType.RS_HIT
	res.hit.CopyFrom(p.makeHit(BoardPoint(1, 1)))

	req = pb.Request()
	req.token = 10
	req.type = pb.RqType.RQ_HIT
	req.hit.CopyFrom(p.makeHit(BoardPoint(0, 1)))

	return {
		'raw-res':	res.SerializeToString(),
		'raw-req':	req.SerializeToString()
	}



class TestProtocol:
	def test_parseResponse(self, examples):
		p = Protocol()
		t = p.parseResponse(examples['raw-res'])

		assert type(t) is BoardPoint
		assert t.x == 1
		assert t.y == 1 

	def test_parseRequest(self, examples):
		p = Protocol()
		t = p.parseRequest(examples['raw-req'])

		assert type(t) is BoardPoint
		assert t.x == 0
		assert t.y == 1 

	def test_makeHitReq(self):
		p = Protocol()
		p.setToken(10)
		t = p.makeHitReq(BoardPoint(2, 2))
		assert type(t) is bytes

	def test_makeRegisterReq(self):
		p = Protocol()
		p.setToken(10)
		t = p.makeRegisterReq('test')
		assert type(t) is bytes
		
	def test_makeUpdateReq(self):
		p = Protocol()
		p.setToken(10)
		t = p.makeUpdateReq()
		assert type(t) is bytes
