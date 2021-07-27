def convertMicrobitValue(array):
	
	return array[0][0]


def marshalStringForBleUartSending(strData):
	
	strPreparedData = strData + '\r\n'
	strPreparedData = strPreparedData.encode('utf-8')
	
	return strPreparedData