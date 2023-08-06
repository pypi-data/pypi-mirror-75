*Settings*							
Library	DateTime						
Library	String						
Library	SeleniumLibrary						
Library	RequestsLibrary											
							
*Variables*							
${BROSWER}	Chrome	# 默认配置为谷歌浏览器					
${MAX WAIT SECOND}	120	# 最长等待时间为10秒					
${MID WAIT SECOND}	3	# 一般等待时间为3秒					
${MIN WAIT SECOND}	1	# 最小等待时间为1秒					
${NOW}	Get Current Date						
							
*Keywords*							
Advance Wait And Assert Element Exist	[Arguments]	${xpath}	${js_path}	${wait_time}			
	[Documentation]	传入xpath,js_path,wait_time，判断元素是否存在，返回优先找到元素的locator，停止等待					
	FOR	${i}	IN RANGE	${wait_time}			
	${count}=	Get Element Count	${xpath}				
	Run Keyword if	${count}>0					
	|Return|	${xpath}					
	${count}=	Execute Javascript	return document.querySelectorAll(Argument[0])	Arguments	${js_path}		
	Run Keyword if	${count}>0					
	|Return|	${js_path}					
	Sleep	1					
	|Return|	${Empty}					
