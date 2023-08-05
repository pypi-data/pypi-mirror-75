from bigbluepy.main import MainBBB

bbb = MainBBB()

_response = bbb.api.getMeetings()

for i in _response.meetings['meeting']:
    print(i)