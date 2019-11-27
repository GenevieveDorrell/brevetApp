import acp_times
import arrow


def test_0km_():
    tim = arrow.utcnow()
    i = acp_times.open_time(400.0, 0.0, tim.isoformat())
    p = tim.isoformat()
    assert i == p
    assert acp_times.close_time(400.0, 0.0, tim.isoformat()) == tim.shift(hours=+1).isoformat()


def test_10km_():
    tim = arrow.utcnow()
    i = acp_times.open_time(400.0, 10.0, tim.isoformat())
    c = tim.shift(hours=+(10/34)).isoformat()
    assert i == c
    assert acp_times.close_time(400.0, 10.0, tim.isoformat()) == tim.shift(hours=+((10/20) + 1)).isoformat()

def test_400km_():
    tim = arrow.utcnow()
    assert acp_times.open_time(400.0, 400.0, tim.isoformat()) == tim.shift(hours=+((200/34)+(200/32))).isoformat()
    assert acp_times.close_time(400.0, 400.0, tim.isoformat()) == tim.shift(hours=+(400/15)).isoformat()

def test_250km_():
    tim = arrow.utcnow()
    assert acp_times.open_time(1000.0, 250.0, tim.isoformat()) == tim.shift(hours=+((200/34)+(50/32))).isoformat()
    assert acp_times.close_time(1000.0, 250.0, tim.isoformat()) == tim.shift(hours=+(250/15)).isoformat()

def test_600km_():
    tim = arrow.utcnow()
    assert acp_times.open_time(600.0, 600.0, tim.isoformat()) == tim.shift(hours=+((200/34)+(200/32)+(200/30))).isoformat()
    assert acp_times.close_time(600.0, 600.0, tim.isoformat()) == tim.shift(hours=+(600/15)).isoformat()

def test_1000km_():
    tim = arrow.utcnow()
    assert acp_times.open_time(1000.0, 1000.0, tim.isoformat()) == tim.shift(hours=+((400/28)+(200/34)+(200/32)+(200/30))).isoformat()
    assert acp_times.close_time(1000.0, 1000.0, tim.isoformat()) == tim.shift(hours=+(600/15)+(400/11.428)).isoformat()



