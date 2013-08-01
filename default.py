### ############################################################################################################
###	#	
### # Project: 			#		SolarMovie.so - by The Highway 2013.
### # Author: 			#		The Highway
### # Version:			#		v0.1.6
### # Description: 	#		http://www.solarmovie.so
###	#	
### ############################################################################################################
### ############################################################################################################
##### Imports #####
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs,urlresolver,urllib,urllib2,re,os,sys,htmllib,string,StringIO,logging,random,array,time,datetime,unicodedata,requests
#import zipfile ### Removed because it caused videos to not play. ###
import HTMLParser, htmlentitydefs
try: 		import StorageServer
except: import storageserverdummy as StorageServer
try: 		from t0mm0.common.addon 				import Addon
except: from t0mm0_common_addon 				import Addon
try: 		from t0mm0.common.net 					import Net
except: from t0mm0_common_net 					import Net
try: 		from sqlite3 										import dbapi2 as sqlite; print "Loading sqlite3 as DB engine"
except: from pysqlite2 									import dbapi2 as sqlite; print "Loading pysqlite2 as DB engine"
try: 		from script.module.metahandler 	import metahandlers
except: from metahandler 								import metahandlers
### 
from teh_tools 		import *
from config 			import *
##### /\ ##### Imports #####
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
__plugin__=ps('__plugin__'); __authors__=ps('__authors__'); __credits__=ps('__credits__'); _addon_id=ps('_addon_id'); _domain_url=ps('_domain_url'); _database_name=ps('_database_name'); _plugin_id=ps('_addon_id')
_database_file=os.path.join(xbmc.translatePath("special://database"),ps('_database_name')+'.db'); 
### 
_addon=Addon(ps('_addon_id'), sys.argv); _plugin=xbmcaddon.Addon(id=ps('_addon_id')) #; _plug=xbmcplugin
addon=_addon
cache = StorageServer.StorageServer(ps('_addon_id'))
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Paths #####
### # ps('')
_addonPath	=xbmc.translatePath(_plugin.getAddonInfo('path'))
_artPath		=xbmc.translatePath(os.path.join(_addonPath,ps('_addon_path_art')))
_datapath 	=_addon.get_profile(); _artIcon		=_addon.get_icon(); _artFanart	=_addon.get_fanart()
##### /\
##### Important Functions with some dependencies #####
def art(f,fe=ps('default_art_ext')): ### for Making path+filename+ext data for Art Images. ###
	return xbmc.translatePath(os.path.join(_artPath,f+fe))
def addst(r,s=''): ## Get Settings
	return _addon.get_setting(r)
def addpr(r,s=''): ## Get Params
	return _addon.queries.get(r,s)
def cFL(t,c=ps('default_cFL_color')): ### For Coloring Text ###
	return '[COLOR '+c+']'+t+'[/COLOR]'
##### /\
##### Settings #####
_setting={}
_setting['debug-enable']=	_debugging			=tfalse(addst("debug-enable"))
_setting['debug-show']	=	_shoDebugging		=tfalse(addst("debug-show"))
_setting['enableMeta']	=	_enableMeta			=tfalse(addst("enableMeta"))
_setting['meta.movie.domain']=ps('meta.movie.domain')
_setting['meta.movie.search']=ps('meta.movie.search')
_setting['meta.tv.domain']=ps('meta.tv.domain')
_setting['meta.tv.search']=ps('meta.tv.search')
_setting['meta.tv.page']=ps('meta.tv.page')
_setting['meta.tv.fanart.url']=ps('meta.tv.fanart.url')
_setting['meta.tv.fanart.url2']=ps('meta.tv.fanart.url2')

##### /\
_artSun=art('sun'); _art404=art('404'); _art150=art('thumb150'); _artDead=art('deadplanet'); GENRES=ps('GENRES'); _default_section_=ps('default_section'); net=Net(); DB=_database_file; BASE_URL=_domain_url;
if (_debugging==True): print 'Addon Path: '+_addonPath
if (_debugging==True): print 'Art Path: '+_artPath
if (_debugging==True): print 'Addon Icon Path: '+_artIcon
if (_debugging==True): print 'Addon Fanart Path: '+_artFanart
### ############################################################################################################
def deadNote(header='',msg='',delay=5000,image=_artDead):
	_addon.show_small_popup(title=header,msg=msg,delay=delay,image=image)
def sunNote(header='',msg='',delay=5000,image=_artSun):
	header=cFL(header,ps('cFL_color')); msg=cFL(msg,ps('cFL_color2'))
	_addon.show_small_popup(title=header,msg=msg,delay=delay,image=image)
def messupText(t,_html=False,_ende=False,_a=False,Slashes=False):
	if (_html==True): t=ParseDescription(HTMLParser.HTMLParser().unescape(t))
	if (_ende==True): t=t.encode('ascii', 'ignore'); t=t.decode('iso-8859-1')
	if (_a==True): t=_addon.decode(t); t=_addon.unescape(t)
	if (Slashes==True): t=t.replace( '_',' ')
	return t
### ############################################################################################################
### ############################################################################################################
##### Queries #####
_param={}
_param['mode'],_param['url']=addpr('mode',''),addpr('url',''); _param['pagesource'],_param['pageurl'],_param['pageno'],_param['pagecount']=addpr('pagesource',''),addpr('pageurl',''),addpr('pageno',0),addpr('pagecount',1)
_param['img']=addpr('img',''); _param['fanart']=addpr('fanart',''); _param['thumbnail'],_param['thumbnail'],_param['thumbnail']=addpr('thumbnail',''),addpr('thumbnailshow',''),addpr('thumbnailepisode','')
_param['section']=addpr('section','movies'); _param['title']=addpr('title',''); _param['year']=addpr('year',''); _param['genre']=addpr('genre','')
_param['by']=addpr('by',''); _param['letter']=addpr('letter',''); _param['showtitle']=addpr('showtitle',''); _param['showyear']=addpr('showyear',''); _param['listitem']=addpr('listitem',''); _param['infoLabels']=addpr('infoLabels',''); _param['season']=addpr('season',''); _param['episode']=addpr('episode','')
_param['pars']=addpr('pars',''); _param['labs']=addpr('labs',''); _param['name']=addpr('name',''); _param['thetvdbid']=addpr('thetvdbid','')
_param['plot']=addpr('plot',''); _param['tomode']=addpr('tomode',''); _param['country']=addpr('country','')
_param['thetvdb_series_id']=addpr('thetvdb_series_id','')
_param['dbid']=addpr('dbid','')

#_param['']=_addon.queries.get('','')
#_param['']=_addon.queries.get('','')
#_param['']=_addon.queries.get('','')
#_param['']=_addon.queries.get('','')
##_param['pagestart']=addpr('pagestart',0)
##### /\

### ############################################################################################################
### ############################################################################################################
def initDatabase():
	print "Building solarmovie Database"
	if ( not os.path.isdir( os.path.dirname(_database_file) ) ): os.makedirs( os.path.dirname( _database_file ) )
	db = sqlite.connect( _database_file )
	cursor = db.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS seasons (season UNIQUE, contents);')
	cursor.execute('CREATE TABLE IF NOT EXISTS favorites (type, name, url, img);')
	db.commit()
	db.close()

### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Player Functions #####
def PlayVideo(url, infoLabels, listitem):
	WhereAmI('@ PlayVideo -- Getting ID From:  %s' % url)
	My_infoLabels=eval(infoLabels)
	#My_infoLabels={ "Title": ShowTitle, "Year": ShowYear, "Plot": ShowPlot, 'IMDbURL': IMDbURL, 'IMDbID': IMDbID, 'IMDb': IMDbID }
	infoLabels={ "Studio": My_infoLabels['Studio'], "ShowTitle": My_infoLabels['ShowTitle'], "Title": My_infoLabels['Title'], "Year": My_infoLabels['Year'], "Plot": My_infoLabels['Plot'], 'IMDbURL': My_infoLabels['IMDbURL'], 'IMDbID': My_infoLabels['IMDbID'], 'IMDb': My_infoLabels['IMDb'] }
	li=xbmcgui.ListItem(_param['title'], iconImage=_param['img'], thumbnailImage=_param['img'])
	match=re.search( '/.+?/.+?/(.+?)/', url) ## Example: http://www.solarmovie.so/link/show/1052387/ ##
	videoId=match.group(1); deb('Solar ID',videoId)
	url=BASE_URL + '/link/play/' + videoId + '/' ## Example: http://www.solarmovie.so/link/play/1052387/ ##
	html=net.http_GET(url).content
	match=re.search( '<iframe.+?src="(.+?)"', html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
	link=match.group(1); link=link.replace('/embed/', '/file/'); deb('hoster link',link)
	#if (_debugging==True): print listitem
	#if (_debugging==True): print infoLabels
	##xbmc.Player( xbmc.PLAYER_CORE_PAPLAYER ).play(stream_url, li)
	##infoLabels.append('url': stream_url)
	li.setInfo(type="Video", infoLabels=infoLabels )
	li.setProperty('IsPlayable', 'true')
	##if (urlresolver.HostedMediaFile(link).valid_url()):
	##else: 
	### _addon.resolve_url(link)
	### _addon.resolve_url(stream_url)
	try: stream_url = urlresolver.HostedMediaFile(link).resolve()
	except: 
		if (_debugging==True): print 'Link URL Was Not Resolved: '+link
		notification("urlresolver.HostedMediaFile(link).resolve()","Failed to Resolve Playable URL.")
		return
	_addon.end_of_directory()
	#xbmc.Player().stop()
	play=xbmc.Player(xbmc.PLAYER_CORE_AUTO) ### xbmc.PLAYER_CORE_AUTO | xbmc.PLAYER_CORE_DVDPLAYER | xbmc.PLAYER_CORE_MPLAYER | xbmc.PLAYER_CORE_PAPLAYER
	play.play(stream_url, li)
	xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)
	#xbmc.sleep(7000)

def PlayTrailer(url):
	sources=[]; url=url.decode('base-64'); WhereAmI('@ PlayVideo:  %s' % url)
	try: 
		hosted_media=urlresolver.HostedMediaFile(url=url)
		sources.append(hosted_media)
		source=urlresolver.choose_source(sources)
		if (source): stream_url=source.resolve()
	except:
		deb('Stream failed to resolve',url); return
	else: stream_url = ''
	try: xbmc.Player().play(stream_url)
	except: 
		deb('Video failed to play',stream_url); return

##### /\
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Weird, Stupid, or Plain up Annoying Functions. #####
def netURL(url): ### Doesn't seem to work.
	return net.http_GET(url).content
def remove_accents(input_str): ### Not even sure rather this one works or not.
	nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
	return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

##### /\
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Menus #####
def mGetItemPage(url):
	deb('Fetching html from Url',url)
	try: html=net.http_GET(url).content
	except: html=''
	if (html=='') or (html=='none') or (html==None) or (html==False): return ''
	else:
		html=HTMLParser.HTMLParser().unescape(html); html=_addon.decode(html); html=_addon.unescape(html); html=ParseDescription(html); html=html.encode('ascii', 'ignore'); html=html.decode('iso-8859-1'); deb('Length of HTML fetched',str(len(html)))
	return html

def mGetDataTest(html,toGet): ## For Testing Only
	resultCnt=0; results={}; debob(toGet)
	for item in toGet:
		item=item.lower();parseMethod=''; parseTag=''; parseTag2=''; parseTag3=''; rCheck=False
		parseTag='<p id="plot_\d+">(.+?)</p>'
		results[item]=(re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
		return results

def mGetDataPlot(html,parseTag='<p id=\"plot_\d+\">(.+?)</p>'): ## Working Temp-Fix
	if ('<p id="plot_' in html):
		try: return (re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
		except: return ''
	else: return ''

def mGetDataGenre(html,parseTag='<a href=".+?watch-.+?-.+?s.html">[\n]\s+(.+?)</a>',ifTag='.html">',startTag='<div class="mediaDescription">',endTag='<div class="buttonsLine">'): ## Think I'll keep this one since it needs the outside part parsed out.
	if (ifTag in html):
		html=(((html.split(startTag)[1])).split(endTag)[0]).strip() ##; deb('Genre',html); return html
		try: results=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)
		except: return ''
		i=0; r=''
		for result in results:
			if (i==0): 	r=result.strip()
			else: 			r=r+', '+result.strip()
			i=i+1
		deb('Genre',r); return r
	else: return ''

def mGetDataCountry(html,parseTag='<a href=".+?s-from.+?.html">(.+?)</a>',ifTag='.html">',startTag='<div class="mediaDescription">',endTag='<div class="buttonsLine">'): ## Think I'll keep this one since it needs the outside part parsed out.
	if (ifTag in html):
		html=(((html.split(startTag)[1])).split(endTag)[0]).strip() ##; deb('Country',html); return html
		try: results=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)
		except: return ''
		i=0; r=''
		for result in results:
			if (i==0): 	r=result.strip()
			else: 			r=r+', '+result.strip()
			i=i+1
		deb('Country',r); return r
	else: return ''

def mGetDataDirector(html,parseTag='<a href="/watch-movies-by-.+?.html">[\n]\s+(.+?)</a>',ifTag='<h4>Director</h4>',startTag='<h4>Director</h4>',endTag='</div>'): ## Think I'll keep this one since it needs the outside part parsed out.
	if (ifTag in html):
		html=(((html.split(startTag)[1])).split(endTag)[0]).strip()
		try: results=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)
		except: return ''
		i=0; r=''
		for result in results:
			if (i==0): 	r=result.strip()
			else: 			r=r+', '+result.strip()
			i=i+1
		deb('Director',r); return r
	else: return ''

def mGetDataCast(html,parseTag='<a href="/watch-movies-with-.+?.html">[\n]\s+(.+?)</a>',ifTag='<h4>Cast</h4>',startTag='<h4>Cast</h4>',endTag='</div>'): ## Think I'll keep this one since it needs the outside part parsed out.
	if (ifTag in html):
		html=(((html.split(startTag)[1])).split(endTag)[0]).strip()
		try: results=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)
		except: return ''
		i=0; r=''
		for result in results:
			if (i==0): 	r=result.strip()
			else: 			r=r+', '+result.strip()
			i=i+1
		deb('Cast',r); return r
	else: return ''

def mGetDataKeywords(html,parseTag='<a href="/watch-movies-tagged-as-.+?.html">[\n]\s+(.+?)</a>',ifTag='<h4>Keywords</h4>',startTag='<h4>Keywords</h4>',endTag='</div>'): ## Think I'll keep this one since it needs the outside part parsed out.
	if (ifTag in html):
		html=(((html.split(startTag)[1])).split(endTag)[0]).strip()
		try: results=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)
		except: return ''
		i=0; r=''
		for result in results:
			if (i==0): 	r=result.strip()
			else: 			r=r+', '+result.strip()
			i=i+1
		deb('Keywords',r); return r
	else: return ''

def mdGetTV(html,toGet):
	resultCnt=0; results={}; debob(toGet)
	for item in toGet:
		item=item.lower();parseMethod=''; parseTag=''; parseTag2=''; parseTag3=''; parsePreResult=''; rCheck=False
		if (item=='result.url'): ### 
			parsePreResult=_setting['meta.tv.page']
			parseTag='<tr><td class="\D+">\d+</td>.+?href="/index.php.+?tab=series.+?id=(\d+)&.+?lid=7">'
			parseMethod='re.compile.prefix'
			if ('>English</td>' in html): rCheck=True
		elif (item=='result.id'): ### 
			parseTag='<tr><td class="\D+">\d+</td>.+?href="/index.php.+?tab=series.+?id=(\d+)&lid=7">' ## &amp; 's were parsed out earlier. ##
			parseMethod='re.compile'
			if ('>English</td>' in html): rCheck=True
		elif (item=='fanart'): ### 
			parsePreResult=_setting['meta.tv.domain']
			parseTag='<tr><td></td><td align=right><a href="(.+?)" target="_blank">View Full Size</a></td></tr>'
			parseMethod='re.compile.group'
			if ('" target="_blank">View Full Size</a></td></tr>' in html): rCheck=True
		elif (item=='thetvdb.episode.overviews'): ### 
			parseTag='<td>Overview: </td>'
			parseTag2='</tr>'
			parseMethod='split'
			deb('get item',item)
			if ('<td>Overview: </td>' in html): rCheck=True
		elif (item=='thetvdb.episode.overview1'): ### 
			parseTag='<textarea rows="10" cols="45" name="Overview_7" style="display: inline">'
			parseTag2='</textarea>'
			parseMethod='split'
			deb('get item',item)
			if ('<td>Overview: </td>' in html): rCheck=True
		elif (item=='thetvdb.episode.overview'): ### 
			parseTag='<textarea rows="10" cols="45" name="Overview_7" style="display: inline">(.+?)</textarea>'
			parseMethod='re.compile'
			deb('get item',item)
			if ('<td>Overview: </td>' in html): rCheck=True
		#else: rCheck=False
		#if (rCheck==False): print html
		deb('rCheck',str(rCheck))
		if (rCheck==True): ## Trying to do away with errors for results that dont contain the requested information.
			if   (parseMethod=='re.compile2'): ## returns 2nd result
				results[item]=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[1].strip()
				if (results[item]==''): re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0].strip()
				resultCnt=resultCnt+1
			elif (parseMethod=='re.compile'): ## returns 1st result
				#results[item]=(re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
				results[item]=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0].strip()
				resultCnt=resultCnt+1
			elif (parseMethod=='re.compile.fanart'): ## returns 1st result
				#results[item]=(re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
				html2=(html.split('<h1>Fan Art</h1>')[1]).split('</table>')[0]
				if ('View Full Size' in html2): results[item]=parsePreResult+re.compile(parseTag, re.IGNORECASE | re.DOTALL).findall(html2)[0].strip()
				else: results[item]=''
				resultCnt=resultCnt+1
			elif (parseMethod=='re.compile.prefix'): ## returns 1st result
				#results[item]=(re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
				try: results[item]=parsePreResult+re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0].strip()
				except: results[item]=''
				resultCnt=resultCnt+1
			elif (parseMethod=='re.compile.group'): ## returns a group of results
				results[item]=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html); resultCnt=resultCnt+1
			elif (parseMethod=='split'):
				results[item]=(((html.split(parseTag)[1])).split(parseTag2)[0]).strip(); resultCnt=resultCnt+1
			elif (parseMethod=='re.search2'): ## returns 2nd result
				match=re.search(parseTag, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
				results[item]=match.group(2); resultCnt=resultCnt+1
			elif (parseMethod=='re.search'): ## returns 1st result
				match=re.search(parseTag, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
				results[item]=match.group(1); resultCnt=resultCnt+1
			elif (parseMethod=='re.search.group'): ## returns a group of results
				match=re.search(parseTag, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
				results[item]=match.group(); resultCnt=resultCnt+1
				#results[item]=match; resultCnt=resultCnt+1  ## Not sure which one to use yet. ##
			else: 
				results[item]=''; resultCnt=resultCnt+1
		else: 
			results[item]=''; resultCnt=resultCnt+1
	if debugging==True: print results
	return results

def mdGetSplitFindGroup(html,ifTag='', parseTag='',startTag='',endTag=''): 
	if (ifTag=='') or (parseTag=='') or (startTag=='') or (endTag==''): return ''
	if (ifTag in html):
		html=(((html.split(startTag)[1])).split(endTag)[0]).strip()
		##deb('Test',html); return html
		try: return re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)
		except: return ''
	else: return ''

def mdGetMovie(html,toGet):
	resultCnt=0; results={}; debob(toGet)
	for item in toGet:
		item=item.lower();parseMethod=''; parseTag=''; parseTag2=''; parseTag3=''; parsePreResult=''; rCheck=False
		if (item=='result.poster'): ### 
			parseTag='<div class="poster">[\n]\s+<a href=".+?" title=".+?"><img class="right_shadow" src="(.+?)" width="\d+" height="\d+" /></a>'
			parseMethod='re.compile'
			if ('<div class="poster">' in html): rCheck=True
		elif (item=='result.url'): ### 
			parsePreResult=_setting['meta.movie.domain']
			parseTag='<div class="poster">[\n]\s+<a href="(.+?)" title=".+?"><img class="right_shadow" src=".+?" width="\d+" height="\d+" /></a>'
			parseMethod='re.compile.prefix'
			if ('<div class="poster">' in html): rCheck=True
		elif (item=='og.image'): ### 
			parseTag='<meta property="og:image" content="(.+?)" />'
			parseMethod='re.compile'
			if ('<meta property="og:image" content="' in html): rCheck=True
		elif (item=='og.image2'): ### 
			parseTag='<meta property="og:image" content="(.+?)" />'
			parseMethod='re.compile2'
			if ('<meta property="og:image" content="' in html): rCheck=True
		elif (item=='og.plot'): ### 
			parseTag='<meta property="og:description" content="(.+?)" />'
			parseMethod='re.compile'
			if ('<meta property="og:description" content="' in html): rCheck=True
		#if (item=='fanart'): ### 
		#	parseTag='<strong>IMDb rating:</strong>[\n]\s+(.+?)\s+\(.+? votes\)'
		#	parseMethod='re.compile.group'
		#	if ('<strong>IMDb rating:</strong>' in html): rCheck=True
		#else: rCheck=False
		deb('rCheck',str(rCheck))
		if (rCheck==True): ## Trying to do away with errors for results that dont contain the requested information.
			if   (parseMethod=='re.compile2'): ## returns 2nd result
				results[item]=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[1].strip()
				if (results[item]==''): re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0].strip()
				resultCnt=resultCnt+1
			elif (parseMethod=='re.compile'): ## returns 1st result
				#results[item]=(re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
				results[item]=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0].strip()
				resultCnt=resultCnt+1
			elif (parseMethod=='re.compile.prefix'): ## returns 1st result
				#results[item]=(re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
				results[item]=parsePreResult+re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0].strip()
				resultCnt=resultCnt+1
			elif (parseMethod=='re.compile.group'): ## returns a group of results
				results[item]=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html); resultCnt=resultCnt+1
			elif (parseMethod=='split'):
				results[item]=(((html.split(parseTag)[1])).split(parseTag2)[0]).strip(); resultCnt=resultCnt+1
			elif (parseMethod=='re.search2'): ## returns 2nd result
				match=re.search(parseTag, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
				results[item]=match.group(2); resultCnt=resultCnt+1
			elif (parseMethod=='re.search'): ## returns 1st result
				match=re.search(parseTag, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
				results[item]=match.group(1); resultCnt=resultCnt+1
			elif (parseMethod=='re.search.group'): ## returns a group of results
				match=re.search(parseTag, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
				results[item]=match.group(); resultCnt=resultCnt+1
				#results[item]=match; resultCnt=resultCnt+1  ## Not sure which one to use yet. ##
			else: 
				results[item]=''; resultCnt=resultCnt+1
		else: 
			results[item]=''; resultCnt=resultCnt+1
	if debugging==True: print results
	return results

def mGetData(html,toGet):
	#if (html=='') or (html=='none') or (html==None) or (html==False): 
	#	deb('mGetData','html is empty')
	#	return None
	resultCnt=0; results={}; debob(toGet)
	for item in toGet:
		item=item.lower();parseMethod=''; parseTag=''; parseTag2=''; parseTag3=''; rCheck=False
		if (item=='plot') or (item=='movieplot') or (item=='showplot'): ### 
			parseTag='<p id="plot_\d+">(.+?)</p>'
			parseMethod='re.compile'
			if ('<p id="plot_' in html): 
				rCheck=True
				print "found: '<p id=\"plot_'"
		elif (item=='imdbrating'): ### 7.3
			parseTag='<strong>IMDb rating:</strong>[\n]\s+(.+?)\s+\(.+? votes\)'
			parseMethod='re.compile'
			if ('<strong>IMDb rating:</strong>' in html): rCheck=True
		##if (item=='description'): ### 
		##	parseTag='<p id="plot_\d+">(.+?)</p>'
		##	parseMethod='re.compile'
		##	if ('<p id="plot_' in html): rCheck=True
		##	#<meta name="description" content="Watch full The Heat movie produced in 2013. Genres are Comedy, Crime, Action." />
		elif (item=='episodeplot'): ### 
			parseTag='<p id="plot_\d+">(.+?)</p>'
			parseMethod='re.compile2'
			if ('<p id="plot_' in html): rCheck=True
		elif (item=='latestepisodeplot'): ### 
			parseTag='<p id="plot_\d+">(.+?)</p>'
			parseMethod='re.compile2'
			if ('<p id="plot_' in html): rCheck=True
		elif (item=='imdbid'): ### 0816711
			parseTag='<strong>IMDb ID:</strong>[\n]\s+<a href=".+?">(\d+)</a>'
			parseMethod='re.compile'
			if ('<strong>IMDb ID:</strong>' in html): rCheck=True
		elif (item=='imdburl'): ### http://anonym.to/?http%3A%2F%2Fwww.imdb.com%2Ftitle%2Ftt0816711%2F
			parseTag='<strong>IMDb ID:</strong>[\n]\s+<a href="(.+?)">\d+</a>'
			parseMethod='re.compile'
			if ('<strong>IMDb ID:</strong>' in html): rCheck=True
		elif (item=='imdbvotes'): ### 2,814
			parseTag='<strong>IMDb rating:</strong>[\n]\s+.+?\s+\((.+?) votes\)'
			parseMethod='re.compile'
			if ('<strong>IMDb rating:</strong>' in html): rCheck=True
		elif (item=='duration'): ### 116 min
			parseTag='<strong>Duration:</strong>[\n]\s+(.+?)<'
			parseMethod='re.compile'
			if ('<strong>Duration:</strong>' in html): rCheck=True
		elif (item=='duration2'):
			parseTag='<strong>Duration:</strong>'
			parseTag2='<'
			parseMethod='strip'
			if ('<strong>Duration:</strong>' in html): rCheck=True
		elif (item=='premiered'): ### June 21, 2013
			parseTag='<strong>Release Date:</strong>[\n]\s+(.+?)\s+[\n]\s+</div>'
			parseMethod='re.compile'
			if ('<strong>Release Date:</strong>' in html): rCheck=True
		elif (item=='premiered2'):
			parseTag='<strong>Release Date:</strong>'
			parseTag2='<'
			parseMethod='strip'
			if ('<strong>Release Date:</strong>' in html): rCheck=True
		elif (item=='reelasedate'): ### June 21, 2013
			parseTag='<strong>Release Date:</strong>[\n]\s+(.+?)\s+[\n]\s+</div>'
			parseMethod='re.compile'
			if ('<strong>Release Date:</strong>' in html): rCheck=True
		elif (item=='reelasedate2'):
			parseTag='<strong>Release Date:</strong>'
			parseTag2='<'
			parseMethod='strip'
			if ('<strong>Release Date:</strong>' in html): rCheck=True
		elif (item=='Votes'): ### 86
			parseTag='<strong>Solar rating:</strong>[\n]\s+<span class="js-votes"[\n]\s+>(\d+\s+votes</span>'
			parseMethod='re.compile'
			if ('<strong>Solar rating:</strong>' in html) and ('<span class="js-votes"' in html) and ('votes</span>' in html): rCheck=True
		elif (item=='coverimage'): ### http://static.solarmovie.so/images/movies/0460681_150x220.jpg
			parseTag='coverImage">.+?src="(.+?)"'
			parseMethod='re.search'
			if ('coverImage">' in html): rCheck=True
		elif (item=='season'): ### 
			parseTag="toggleSeason\('(\d+)'\)"
			parseMethod='re.search'
			if ('toggleSeason' in html): rCheck=True
		elif (item=='seasons'): ### 
			parseTag="toggleSeason\('(\d+)'\)"
			parseMethod='re.search.group'
			if ('toggleSeason' in html): rCheck=True
		elif (item=='episode'): ### 
			parseTag='<span class="epname">[\n].+?<a href="(.+?)"[\n]\s+title=".+?">(.+?)</a>[\n]\s+<a href="/.+?/season-(\d+)/episode-(\d+)/" class=".+?">[\n]\s+(\d+) links</a>'
			parseMethod='re.compile'
			if ('<span class="epname">' in html) and (' links</a>' in html): rCheck=True
		elif (item=='episodes'): ### 
			parseTag='<span class="epname">[\n].+?<a href="(.+?)"[\n]\s+title=".+?">(.+?)</a>[\n]\s+<a href="/.+?/season-(\d+)/episode-(\d+)/" class=".+?">[\n]\s+(\d+) links</a>'
			parseMethod='re.compile.group'
			##episodes=re.compile('<span class="epname">[\n].+?<a href="(.+?)"[\n]\s+title=".+?">(.+?)</a>[\n]\s+<a href="/.+?/season-(\d+)/episode-(\d+)/" class=".+?">[\n]\s+(\d+) links</a>', re.IGNORECASE | re.MULTILINE | re.DOTALL).findall(html) #; if (_debugging==True): print episodes
			##for ep_url, episode_name, season_number, episode_number, num_links in episodes:
			if ('<span class="epname">' in html): rCheck=True
		else: rCheck=False
		#
		### Year
		#
		#                    Fantasy</a>                                    produced in
		#        <a href="/tv/watch-tv-shows-2005.html">
		#                2005</a>
		#
		### Country
		#                    [<a href="/tv/tv-shows-from-usa.html">USA</a>]
		#
		### Latest Episode
		#            <div class="mediaDescription latestTvEpisode">
		#
		#        <h5>Latest Episode:
		#            <a href="/tv/supernatural-2005/season-8/episode-23/">
		#                Sacrifice                (<span>s08e23</span>)</a>
		#              <em class="releaseDate">May 15, 2013</em>
		#        </h5>
		#
		#<p id="plot_476403">Sam and Dean capture Crowley to finish the trials and close the gates of Hell. Castiel and Metatron continue the trials to close the gates of Heaven. Sam is left with a huge decision.</p>
		#                        </div>
		### Genres
		#<meta name="description" content="Watch full The Heat movie produced in 2013. Genres are Comedy, Crime, Action." />
		#
		#
		#
		#
		#
		#
		#
		#
		deb('rCheck',str(rCheck))
		if (rCheck==True): ## Trying to do away with errors for results that dont contain the requested information.
			if (parseMethod=='re.compile2'): ## returns 2nd result
				try: results[item]=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[1].strip()
				except: results[item]=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0].strip()
				resultCnt=resultCnt+1
			elif (parseMethod=='re.compile'): ## returns 1st result
				#results[item]=(re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
				results[item]=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0].strip()
				resultCnt=resultCnt+1
			elif (parseMethod=='re.compile.group'): ## returns a group of results
				results[item]=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html); resultCnt=resultCnt+1
			elif (parseMethod=='split'):
				results[item]=(((html.split(parseTag)[1])).split(parseTag2)[0]).strip(); resultCnt=resultCnt+1
			elif (parseMethod=='re.search2'): ## returns 2nd result
				match=re.search(parseTag, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
				results[item]=match.group(2); resultCnt=resultCnt+1
			elif (parseMethod=='re.search'): ## returns 1st result
				match=re.search(parseTag, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
				results[item]=match.group(1); resultCnt=resultCnt+1
			elif (parseMethod=='re.search.group'): ## returns a group of results
				match=re.search(parseTag, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
				results[item]=match.group(); resultCnt=resultCnt+1
				#results[item]=match; resultCnt=resultCnt+1  ## Not sure which one to use yet. ##
			else: 
				results[item]=''; resultCnt=resultCnt+1
		else: 
			results[item]=''; resultCnt=resultCnt+1
	if debugging==True: print results
	return results

def listLinks(section, url, showtitle='', showyear=''): ### Menu for Listing Hosters (Host Sites of the actual Videos)
	WhereAmI('@ the Link List: %s' % url); sources=[]; listitem=xbmcgui.ListItem()
	if (url==''): return
	html=net.http_GET(url).content
	html=html.encode("ascii", "ignore")
	#if (_debugging==True): print html
	if  ( section == 'tv'): ## TV Show
		match=re.compile(ps('LLinks.compile.show_episode.info'), re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]
		### <title>Watch The Walking Dead Online for Free - Prey - S03E14 - 3x14 - SolarMovie</title>
		if (_debugging==True): print match
		if (match==None):  return
		#ShowYear=showyear
		ShowYear=_param['year']
		ShowTitle=match[0].strip(); EpisodeTitle=match[1].strip(); Season=match[2].strip(); Episode=match[3].strip()
		ShowTitle=HTMLParser.HTMLParser().unescape(ShowTitle); ShowTitle=ParseDescription(ShowTitle); ShowTitle=ShowTitle.encode('ascii', 'ignore'); ShowTitle=ShowTitle.decode('iso-8859-1')
		EpisodeTitle=HTMLParser.HTMLParser().unescape(EpisodeTitle); EpisodeTitle=ParseDescription(EpisodeTitle); EpisodeTitle=EpisodeTitle.encode('ascii', 'ignore'); EpisodeTitle=EpisodeTitle.decode('iso-8859-1')
		if ('<p id="plot_' in html):
			ShowPlot=(re.compile(ps('LLinks.compile.show.plot'), re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
			ShowPlot=HTMLParser.HTMLParser().unescape(ShowPlot); ShowPlot=ParseDescription(ShowPlot); ShowPlot=ShowPlot.encode('ascii', 'ignore'); ShowPlot=ShowPlot.decode('iso-8859-1')
		else: ShowPlot=''
		match=re.compile(ps('LLinks.compile.imdb.url_id'), re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]
		if (_debugging==True): print match
		(IMDbURL,IMDbID)=match
		IMDbURL=IMDbURL.strip(); IMDbID=IMDbID.strip()
		My_infoLabels={ "Studio": ShowTitle+'  ('+ShowYear+'):  '+Season+'x'+Episode+' - '+EpisodeTitle, "Title": ShowTitle, "ShowTitle": ShowTitle, "Year": ShowYear, "Plot": ShowPlot, 'Season': Season, 'Episode': Episode, 'EpisodeTitle': EpisodeTitle, 'IMDbURL': IMDbURL, 'IMDbID': IMDbID, 'IMDb': IMDbID }
		listitem.setInfo(type="Video", infoLabels=My_infoLabels )
		#match=re.search('bradcramp.+?href=".+?>(.+?)<.+?href=".+?>        Season (.+?) .+?[&nbsp;]+Episode (.+?)<', html, re.MULTILINE | re.IGNORECASE | re.DOTALL)
		#if (_debugging==True): print match
		#if (match==None): return
		#listitem.setInfo('video', {'TVShowTitle': match.group(1), 'Season': int(match.group(2)), 'Episode': int(match.group(3)) } )
	else:	#################### Movie
		#match=re.search('float:left;">(.+?)<em.+?html">[\n]*(.+?)</a>', html, re.MULTILINE | re.IGNORECASE | re.DOTALL)
		#<title>Watch Full The Dark Knight (2008)  Movie Online - Page 1 - SolarMovie</title>
		#match=re.search('<title>Watch Full (.+?) \((.+?)\) .+?</title>', html, re.MULTILINE | re.IGNORECASE | re.DOTALL)
		match=re.compile(ps('LLinks.compile.show.title_year'), re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]
		if (_debugging==True): print match
		if (match==None): return
		ShowYear=match[1].strip(); ShowTitle=match[0].strip()
		ShowTitle=HTMLParser.HTMLParser().unescape(ShowTitle); ShowTitle=ParseDescription(ShowTitle); ShowTitle=ShowTitle.encode('ascii', 'ignore'); ShowTitle=ShowTitle.decode('iso-8859-1')
		ShowPlot=(re.compile(ps('LLinks.compile.show.plot'), re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
		ShowPlot=HTMLParser.HTMLParser().unescape(ShowPlot); ShowPlot=ParseDescription(ShowPlot); ShowPlot=ShowPlot.encode('ascii', 'ignore'); ShowPlot=ShowPlot.decode('iso-8859-1')
		match=re.compile(ps('LLinks.compile.imdb.url_id'), re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]
		if (_debugging==True): print match
		(IMDbURL,IMDbID)=match
		IMDbURL=IMDbURL.strip(); IMDbID=IMDbID.strip()
		My_infoLabels={ "Studio": ShowTitle+'  ('+ShowYear+')', "Title": ShowTitle, "ShowTitle": ShowTitle, "Year": ShowYear, "Plot": ShowPlot, 'IMDbURL': IMDbURL, 'IMDbID': IMDbID, 'IMDb': IMDbID }
		##liz.setInfo( type="Video", infoLabels={ "Title": showtitle, "Studio": Studio } )
		listitem.setInfo(type="Video", infoLabels=My_infoLabels )
		#listitem.setInfo('video', {'Title': match.group(1).strip(), 'Year': int(match.group(2).strip())} )
	match =  re.compile(ps('LLinks.compile.hosters'), re.MULTILINE | re.DOTALL | re.IGNORECASE).findall(html)
	#match =  re.compile('<tr id=.+?href="(.+?)">(.+?)<.+?class="qualityCell">(.+?)<', re.MULTILINE | re.DOTALL | re.IGNORECASE).findall(html)
	### print ' length of match is %d' % len(match)
	if (len(match) > 0):
		count=1
		for url, host, quality, age in match:
			host=host.strip(); quality=quality.strip(); name=str(count)+". "+host+' - [[B]'+quality+'[/B]] - ([I]'+age+'[/I])'
			if urlresolver.HostedMediaFile(host=host, media_id='xxx'):
				img=ps('Hosters.icon.url')+host
				My_infoLabels['quality']=quality
				My_infoLabels['age']=age
				My_infoLabels['host']=host
				#_addon.add_item(url,{'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  name})
				_addon.add_directory({'section': section, 'img': _param['img'], 'mode': 'PlayVideo', 'url': url, 'quality': quality, 'age': age, 'infoLabels': My_infoLabels, 'listitem': listitem}, {'title':  name}, img=img, is_folder=False)
				#_addon.add_item({'mode': 'PlayVideo', 'url': url, 'quality': quality, 'age': age, 'infoLabels': My_infoLabels, 'listitem': listitem}, {'title':  name}, img=img, is_folder=False)
				#_addon.add_video_item({'mode': 'PlayVideo', 'url': url, 'quality': quality, 'age': age, 'infoLabels': My_infoLabels, 'listitem': listitem}, {'title':  name}, img=img)
				##_addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  name})
				count=count+1 
		_addon.end_of_directory()
	else: return

def Menu_BrowseByGenre(section=_default_section_):
	url=''; WhereAmI('@ the Genre Menu')#print 'Browse by genres screen'
	for genre in GENRES:
		if section == ps('section.movie'): 	url=_domain_url+ps('BrowseByGenre.movie.url1')+(genre.lower())+ps('BrowseByGenre.movie.url2')
		else: 															url=_domain_url+ps('BrowseByGenre.tv.url1')		+(genre.lower())+ps('BrowseByGenre.tv.url2')
		_addon.add_directory({'section': section,'mode': 'GetTitles','url': url,'genre': genre,'pageno': '1','pagecount': '3'}, {'title':  genre},img=_artSun,fanart=_artFanart)
	_addon.end_of_directory()

def Menu_BrowseByYear(section=_default_section_):
	url=''; WhereAmI('@ the Year Menu'); EarliestYear=(ps('BrowseByYear.earliestyear') - 1) #1929 #1930 ### This is set to 1 year earlier so that it will display too ### 
	try: thisyear=int(datetime.date.today().strftime("%Y"))
	except: thisyear=ps('BrowseByYear.thisyear')
	for year in range(thisyear, EarliestYear, ps('BrowseByYear.range.by')):
		if section == ps('section.movie'): 	url=_domain_url+ps('BrowseByYear.movie.url1')	+str(year)+ps('BrowseByYear.movie.url2')
		else: 															url=_domain_url+ps('BrowseByYear.tv.url1')		+str(year)+ps('BrowseByYear.tv.url2')
		_addon.add_directory({'section': section,'mode': 'GetTitles', 'url': url,'year': year,'pageno': '1','pagecount': '3'}, {'title':  str(year)},img=_artSun,fanart=_artFanart)
	_addon.end_of_directory()

##def listItems(section=_default_section_, url='', html='', episode=False, startPage='1', numOfPages='1', genre='', year='', stitle=''): # List: Movies or TV Shows
def listItems(section=_default_section_, url='', startPage='1', numOfPages='1', genre='', year='', stitle='', season='', episode='', html='', chck=''): # List: Movies or TV Shows
	if (url==''): return
	#if (chck=='Latest'): url=url+chr(35)+'latest'
	WhereAmI('@ the Item List -- url: %s' % url)
	last=2; start=int(startPage); end=(start+int(numOfPages)); html=''; html_last=''; nextpage=startPage
	try: html_=net.http_GET(url).content
	except: 
		try: html_=getURL(url)
		except: 
			try: html_=getURLr(url,_domain_url)
			except: html_=''
	#print html_
	if (html_=='') or (html_=='none') or (html_==None): 
		deb('Error','Problem with page'); deadNote('Results:  '+section,'No results were found.')
		return
	pmatch=re.findall(ps('LI.page.find'), html_)
	if pmatch: last=pmatch[-1]
	for page in range(start,min(last,end)):
		if (int(startPage)> 1): pageUrl=url+ps('LI.page.param')+startPage
		else: pageUrl=url
		try: 
			try: html_last=net.http_GET(pageUrl).content
			except: 
				try: html_=getURL(url)
				except: t=''
			if (_shoDebugging==True) and (html_last==''): deadNote('Testing','html_last is empty')
			if (html_last in html): t=''
			else: html=html+'\r\n'+html_last
			##if (_debugging==True): print html_last
		except: t=''
	if (ps('LI.nextpage.check') in html_last): 
		if (_debugging==True): print 'A next-page has been found.'
		nextpage=re.findall(ps('LI.nextpage.match'), html_last)[0] #nextpage=re.compile('<li class="next"><a href="http://www.solarmovie.so/.+?.html?page=(\d+)"></a></li>').findall(html_last)[0]
		if (int(nextpage) > end) or (end < last): ## Do Show Next Page Link ##
			if (_debugging==True): print 'A next-page is being added.'
			_addon.add_directory({'mode': 'GetTitles', 'url': url, 'pageno': nextpage, 'pagecount': numOfPages}, {'title': ps('LI.nextpage.name')}, img=art('icon-next'))
	##	### _addon.add_directory({'mode': 'GetTitles', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': 'Next...'})
	##html=nolines(html)
	html=ParseDescription(html); html=remove_accents(html) #if (_debugging==True): print html
	if (section==ps('section.tv')) and (season=='') and (episode==''): ## TV Show
		deb('listItems >> ',section); deb('listItems >> chck',chck)
		if   (chck==ps('LI.tv.popular.new.check')): 	html=(html.split(ps('LI.tv.latest.split1'			))[1]).split(ps('LI.tv.latest.split2'))[0]
		elif (chck==ps('LI.tv.popular.all.check')): 	html=(html.split(ps('LI.tv.popular.all.split1'))[1]).split(ps('LI.tv.popular.all.split2'))[0]
		elif (chck==ps('LI.tv.latest.check')): 				html=(html.split(ps('LI.tv.popular.new.split1'))[1]).split(ps('LI.tv.popular.new.split2'))[0]
		iitems=re.compile(ps('LI.tv.match.items'), re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)
		if (iitems==None):
			deb('Item Results','None Found'); deadNote('Results:  '+section,'No results were found.')
		for name, item_url, thumbnail, year in iitems:
			contextMenuItems=[]; name=ParseDescription(HTMLParser.HTMLParser().unescape(name)); name=name.encode('ascii', 'ignore'); name=name.decode('iso-8859-1'); name=name.strip() #; name = remove_accents(name)
			name=_addon.decode(name); name=_addon.unescape(name)
			try: deb('listItems >> '+section+' >> '+name, item_url)
			except: print item_url
			##### Right Click Menu for: TV #####
			contextMenuItems.append((ps('cMI.showinfo.name'),ps('cMI.showinfo.url')))
			if os.path.exists(xbmc.translatePath(ps('special.home.addons'))+ps('cMI.1ch.search.folder')):
				contextMenuItems.append((ps('cMI.1ch.search.name'), 				ps('cMI.1ch.search.url') 				% (ps('cMI.1ch.search.plugin')			, ps('cMI.1ch.search.section.tv'), name)))
			if os.path.exists(xbmc.translatePath(ps('special.home.addons'))+ps('cMI.primewire.search.folder')):
				contextMenuItems.append((ps('cMI.primewire.search.name'), 	ps('cMI.primewire.search.url') 	% (ps('cMI.primewire.search.plugin'), ps('cMI.primewire.search.section.tv'), name)))
			contextMenuItems.append((ps('cMI.airdates.find.name'), 			ps('cMI.airdates.find.url') % (sys.argv[0],ps('cMI.airdates.find.mode'),urllib.quote_plus(name))))
			##### Right Click Menu for: TV ##### /\ #####
			if (chck==ps('LI.tv.latest.check')):
				showTitle, season_number, episode_number, episode_name = re.compile(ps('LI.tv.latest.match.items'), re.IGNORECASE | re.DOTALL).findall('__'+name+'__')[0] #Unsealed: Conspiracy Files s01e14 Fake World Leaders
				showTitle=showTitle.strip(); season_number=season_number.strip(); episode_number=episode_number.strip(); episode_name=episode_name.strip()
				if (_debugging==True): deb('name',name); deb('year',year)
				labs={}
				labs['fanart']=_artFanart
				labs['poster']=labs['image']=labs['thumbnail']=thumbnail; labs['year']=year
				labs['Season']=season_number; labs['EpisodeNumber']=episode_number; labs['Episode']=episode_name; labs['EpisodeTitle']=episode_name
				ihtml=mGetItemPage(_domain_url+item_url)
				labs['Country']=mGetDataCountry(ihtml)
				labs['Rating']=mGetData(ihtml,['imdbrating'])['imdbrating']; labs['Votes']=mGetData(ihtml,['imdbvotes'])['imdbvotes']; labs['RatingAndVotes']=labs['Rating']+' / '+'rating.max'+' ('+labs['Votes']+' Votes)'
				labs['Genre']=mGetDataGenre(ihtml); labs['Director']=mGetDataDirector(ihtml); labs['Cast']=mGetDataCast(ihtml); labs['Keywords']=mGetDataKeywords(ihtml)
				##labs['plot']=mGetData(ihtml,['plot'])['plot']
				labs['TVShowPlot']=mGetData(ihtml,['plot'])['plot']
				labs['EpisodePlot']=mGetData(ihtml,['episodeplot'])['episodeplot']
				labs['plot']=labs['EpisodePlot']
				if (labs['plot']==''): labs['plot']=labs['TVShowPlot']
				labs['PlotOutline']=labs['TVShowPlot']
				labs['Premiered']=mGetData(ihtml,['premiered2'])['premiered2']
				if (labs['Premiered']==''): labs['Premiered']=mGetData(ihtml,['premiered'])['premiered']
				labs['DateReleased']=labs['Release Date']=labs['Aired Date']=labs['Date Aired']=labs['Aired']=labs['Date Posted']=labs['Date']=labs['Premiered']
				if (labs['Genre'] is not ''): 		labs['plot']=labs['plot']+'[CR]Genre:  ['+		labs['Genre']	+']'
				if (labs['Country'] is not ''): 	labs['plot']=labs['plot']+'[CR]Country:  ['+	labs['Country']+']'
				if (labs['Director'] is not ''): 	labs['plot']=labs['plot']+'[CR]Director:  ['+	labs['Director']+']'
				if (labs['Cast'] is not ''): 			labs['plot']=labs['plot']+'[CR]Cast:  ['+			labs['Cast']+']'
				if (labs['Premiered'] is not ''): 			labs['plot']=labs['plot']+'[CR]Premiered:  ['+labs['Premiered']+']'
				if (labs['Rating'] is not '') and (labs['Votes'] is not ''): 			labs['plot']=labs['plot']+'[CR]Rating:  ['+labs['Rating']+' ('+labs['Votes']+' Votes)]'
				labs['TVShowTitle']=showTitle; labs['title']=cFL(showTitle+'  ('+cFL(year,ps('cFL_color2'))+')',ps('cFL_color'))
				if (labs['Country'] is not ''): labs['title']=labs['title']+cFL('  ['+cFL(labs['Country'],ps('cFL_color3'))+']',ps('cFL_color'))
				labs['title']=labs['title']+'[CR]'
				if (season_number is not '') and (episode_number is not ''): labs['title']=labs['title']+'  '+cFL(season_number+cFL('x',ps('cFL_color4'))+episode_number,ps('cFL_color5'))
				if (episode_name is not ''): labs['title']=labs['title']+' - '+cFL(episode_name,ps('cFL_color4'))
				pars={'mode': 'GetLinks', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': showTitle, 'year': year, 'season': season_number, 'episode': episode_number, 'episodetitle': episode_name, 'fanart': labs['fanart'] }
				#set_view('episodes',515,True)
				try: _addon.add_directory(pars, labs, img=labs['thumbnail'], fanart=labs['fanart'], contextmenu_items=contextMenuItems)
				except: 
					labs['title']=showTitle+'  ('+year+')'
					#uname=name; name='[Unknown]'; _addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': showTitle, 'year': year, 'season': season_number, 'episode': episode_number, 'episodetitle': episode_name }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
					try: uname=name; name='[Unknown]'; _addon.add_directory(pars, labs, img=thumbnail, contextmenu_items=contextMenuItems)
					except: t=''
			else:
				_enableMeta=False ### Temp Fix to keep people from accidently using it. ###
				if (_enableMeta==True): ### Doesn't work currently. ###
					metaget=metahandlers.MetaData(); meta=metaget.get_meta('tvshow', name, year=year)
					if (meta['imdb_id']=='') and (meta['tvdb_id']==''):
						meta=metaget.get_meta('tvshow', name)
						#try: 
						_addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': meta['cover_url'], 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=meta['cover_url'], fanart=meta['backdrop_url'], contextmenu_items=contextMenuItems)
						#except: 
						#	uname=name; name='[Unknown]'
						#	try: _addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': meta['cover_url'], 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=meta['cover_url'], fanart=meta['backdrop_url'], contextmenu_items=contextMenuItems)
						#	except: _addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail)
					else:
						#try: 
						_addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
						#except: 
						#	uname=name; name='[Unknown]'; _addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail)
				else: ### Display without MetaData. ###
					labs={}; pars={'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }; labs['fanart']=''
					labs['poster']=labs['image']=labs['thumbnail']=thumbnail; labs['year']=year
					labs['name']=name
					ihtml=mGetItemPage(_domain_url+item_url)
					labs['Genre']=mGetDataGenre(ihtml); labs['Rating']=mGetData(ihtml,['imdbrating'])['imdbrating']; labs['Votes']=mGetData(ihtml,['imdbvotes'])['imdbvotes']; labs['RatingAndVotes']=labs['Rating']+' / 10 ('+labs['Votes']+' Votes)'
					labs['Country']=mGetDataCountry(ihtml); labs['Director']=mGetDataDirector(ihtml); labs['Cast']=mGetDataCast(ihtml); labs['Keywords']=mGetDataKeywords(ihtml)
					labs['plot']=mGetData(ihtml,['plot'])['plot']; labs['imdbid']=mGetData(ihtml,['imdbid'])['imdbid']
					drhtml=mGetItemPage(_setting['meta.tv.search']+labs['imdbid']) ## metadata >> movie >> results
					#dbhtml_url=mdGetTV(drhtml,['result.url'])['result.url']
					labs['thetvdbid']=mdGetTV(drhtml,['result.id'])['result.id']
					if (labs['thetvdbid']=='') or (labs['thetvdbid']=='none') or (labs['thetvdbid']==None) or (labs['thetvdbid']==False): labs['fanart']=''
					else: 
						pars['thetvdb_series_id']=labs['thetvdbid']
						labs['fanart']=ps('meta.tv.fanart.url')+labs['thetvdbid']+ps('meta.tv.fanart.url2')
						if (labs['thumbnail']=='') or (labs['thumbnail']==ps('domain.thumbnail.default')):
							labs['poster']=labs['image']=labs['thumbnail']=ps('meta.tv.poster.url')+labs['thetvdbid']+ps('meta.tv.poster.url2')
					if (labs['fanart']=='') or (labs['fanart']=='none') or (labs['fanart']==None): labs['fanart']=_artFanart
					if (labs['Genre'] is not ''): 		labs['plot']=labs['plot']+'[CR]Genre:  ['	+labs['Genre']	+']'
					if (labs['Country'] is not ''): 	labs['plot']=labs['plot']+'[CR]Country:  ['+labs['Country']+']'
					if (labs['Director'] is not ''): 	labs['plot']=labs['plot']+'[CR]Director:  ['+labs['Director']+']'
					if (labs['Cast'] is not ''): 			labs['plot']=labs['plot']+'[CR]Cast:  ['+labs['Cast']+']'
					if (labs['Rating'] is not '') and (labs['Votes'] is not ''): 			labs['plot']=labs['plot']+'[CR]Rating:  ['+labs['Rating']+' ('+labs['Votes']+' Votes)]'
					labs['TVShowTitle']=name
					labs['title']=cFL(name+'  ('+cFL(year,ps('cFL_color2'))+')',ps('cFL_color'))
					if (labs['Country'] is not ''): labs['title']=labs['title']+cFL('  ['+cFL(labs['Country'],ps('cFL_color3'))+']',ps('cFL_color'))
					pars['plot']=labs['plot']
					pars['Country']=labs['Country']
					pars['fanart']=labs['fanart']
					if (labs['thetvdbid']=='') or (labs['thetvdbid']=='none') or (labs['thetvdbid']==None) or (labs['thetvdbid']==False): pars['thetvdbid']=''
					else: pars['thetvdbid']=labs['thetvdbid']
					#contextMenuItems.append(('-'+ps('cMI.airdates.find.name'), 			ps('cMI.airdates.find.url') % (sys.argv[0],ps('cMI.airdates.find.mode'),urllib.quote_plus(name))))
					contextMenuItems.append((ps('cMI.favorites.tv.add.name'), 	 ps('cMI.favorites.tv.add.url') % (sys.argv[0],ps('cMI.favorites.tv.add.mode'),section,urllib.quote_plus(name),year,urllib.quote_plus(labs['thumbnail']),urllib.quote_plus(labs['fanart']),urllib.quote_plus(labs['Country']),urllib.quote_plus(labs['plot']),urllib.quote_plus(labs['Genre']),urllib.quote_plus(_domain_url + item_url), labs['thetvdbid'] )))
					try: _addon.add_directory(pars, labs, img=labs['thumbnail'], fanart=labs['fanart'], contextmenu_items=contextMenuItems)
 					#try: _addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
					except: 
						#uname=name; name='[Unknown]'; _addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
						try: uname=name; name='[Unknown]'; _addon.add_directory(pars, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
						except: t=''
		if (chck==ps('LI.tv.latest.check')): 		set_view('episodes' ,ps('setview.tv.latestepisodes'),True)
		else: 																	set_view('tvshows'	,ps('setview.tv'),True)
		_addon.end_of_directory(); return
	#elif (section==ps('section.tv')) and (episode==''): ## Season
	#	set_view('seasons',515); _addon.end_of_directory(); return
	#elif (section==ps('section.tv')): ## Episode
	#	set_view('episodes',515); _addon.end_of_directory(); return
	elif (section==ps('section.movie')): ## Movie
		deb('listItems >> ',section); deb('listItems >> chck',chck)
		##set_view('movies',515)
		####xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
		##xbmc.executebuiltin("Container.SetSortMethod(%s)" % xbmcplugin.SORT_METHOD_LABEL)
		if   (chck==ps('LI.movies.popular.new.check')): 	html=(html.split(ps('LI.movies.popular.new.split1'	))[1]).split(ps('LI.movies.popular.new.split2'	))[0]
		elif (chck==ps('LI.movies.popular.hd.check')): 		html=(html.split(ps('LI.movies.popular.hd.split1'		))[1]).split(ps('LI.movies.popular.hd.split2'		))[0]
		elif (chck==ps('LI.movies.popular.other.check')): html=(html.split(ps('LI.movies.popular.other.split1'))[1]).split(ps('LI.movies.popular.other.split2'))[0]
		elif (chck==ps('LI.movies.latest.check')): 				html=(html.split(ps('LI.movies.latest.split1'				))[1]).split(ps('LI.movies.latest.split2'				))[0]
		#elif (chck=='Popular'): ## I guess this isnt used for movies atm.
		iitems=re.compile(ps('LI.movies.match.items'), re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)
		if (iitems==None):
			deb('Item Results','None Found'); deadNote('Results:  '+section,'No results were found.')
		for name, item_url, thumbnail, year in iitems:
			contextMenuItems=[]; name=ParseDescription(HTMLParser.HTMLParser().unescape(name)); name=name.encode('ascii', 'ignore'); name=name.decode('iso-8859-1') #; name = remove_accents(name)
			name=_addon.decode(name); name=_addon.unescape(name)
			try: deb('listItems >> '+section+' >> '+name, item_url)
			except: print item_url
			##### Right Click Menu for: MOVIE #####
			contextMenuItems.append(('Show Information', 			'XBMC.Action(Info)'))
			if os.path.exists(xbmc.translatePath(ps('special.home.addons'))+ps('cMI.1ch.search.folder')):
				contextMenuItems.append((ps('cMI.1ch.search.name'), 					ps('cMI.1ch.search.url') 				% (ps('cMI.1ch.search.plugin'), 			ps('cMI.1ch.search.section'), 			name)))
			if os.path.exists(xbmc.translatePath(ps('special.home.addons'))+ps('cMI.primewire.search.folder')):
				contextMenuItems.append((ps('cMI.primewire.search.name'), 		ps('cMI.primewire.search.url') 	% (ps('cMI.primewire.search.plugin'), ps('cMI.primewire.search.section'), name)))
			##### Right Click Menu for: MOVIE ##### /\ #####
			ihtml=mGetItemPage(_domain_url+item_url)
			##debob(ihtml)
			##plot=mGetData(ihtml,['plot'])['plot']
			##plot=mGetDataTest(ihtml,['plot'])['plot']
			#plot=mGetDataPlot(ihtml)
			#if (plot==None) or (plot=='none') or (plot==False): plot=''
			labs={}; pars={'mode': 'GetLinks', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }
			labs['poster']=labs['image']=labs['thumbnail']=thumbnail; labs['year']=year; labs['Country']=mGetDataCountry(ihtml)
			labs['Rating']=mGetData(ihtml,['imdbrating'])['imdbrating']; labs['Votes']=mGetData(ihtml,['imdbvotes'])['imdbvotes']; labs['RatingAndVotes']=labs['Rating']+' / '+ps('rating.max')+' ('+labs['Votes']+' Votes)'
			labs['Genre']=mGetDataGenre(ihtml); labs['Director']=mGetDataDirector(ihtml); labs['Cast']=mGetDataCast(ihtml); labs['Keywords']=mGetDataKeywords(ihtml)
			labs['PlotOutline']=labs['plot']=mGetData(ihtml,['plot'])['plot']; labs['imdbid']=mGetData(ihtml,['imdbid'])['imdbid']
			drhtml=mGetItemPage(_setting['meta.movie.search']+labs['imdbid']) ## metadata >> movie >> results
			dbhtml_url=mdGetMovie(drhtml,['result.url'])['result.url']; dbhtml=mGetItemPage(dbhtml_url) ## metadata >> movie >> results >> page
			if (labs['plot']==''): labs['plot']=mdGetMovie(dbhtml,['og.plot'])['og.plot']
			if (labs['image']==ps('domain.thumbnail.default')):  ## Default // No - Image. ##
				labs['poster']=labs['image']=labs['thumbnail']=mdGetMovie(dbhtml,['og.image'])['og.image']
			labs['fanart']=mdGetMovie(dbhtml,['og.image2'])['og.image2']
			if (labs['fanart']=='') or (labs['fanart']=='none') or (labs['fanart']==None): labs['fanart']=mdGetMovie(dbhtml,['og.image'])['og.image']
			if (labs['fanart']=='') or (labs['fanart']=='none') or (labs['fanart']==None): labs['fanart']=_artFanart
			if (labs['Genre'] is not ''): 		labs['plot']=labs['plot']+'[CR]Genre:  ['	+labs['Genre']	+']'
			if (labs['Country'] is not ''): 	labs['plot']=labs['plot']+'[CR]Country:  ['+labs['Country']+']'
			if (labs['Director'] is not ''): 	labs['plot']=labs['plot']+'[CR]Director:  ['+labs['Director']+']'
			if (labs['Cast'] is not ''): 			labs['plot']=labs['plot']+'[CR]Cast:  ['+labs['Cast']+']'
			if (labs['Rating'] is not '') and (labs['Votes'] is not ''): 			labs['plot']=labs['plot']+'[CR]Rating:  ['+labs['Rating']+' ('+labs['Votes']+' Votes)]'
			labs['TVShowTitle']=name; labs['title']=cFL(name+'  ('+cFL(year,ps('cFL_color2'))+')',ps('cFL_color'))
			if (labs['Country'] is not ''): labs['title']=labs['title']+cFL('  ['+cFL(labs['Country'],ps('cFL_color3'))+']',ps('cFL_color'))
			contextMenuItems.append((ps('cMI.favorites.tv.add.name'), 	 ps('cMI.favorites.movie.add.url') % (sys.argv[0],ps('cMI.favorites.tv.add.mode'),section,urllib.quote_plus(name),year,urllib.quote_plus(labs['thumbnail']),urllib.quote_plus(labs['fanart']),urllib.quote_plus(labs['Country']),urllib.quote_plus(labs['plot']),urllib.quote_plus(labs['Genre']),urllib.quote_plus(_domain_url + item_url) )))
			#contextMenuItems.append(('Favorites - Add', 'XBMC.RunPlugin(%s?mode=%s&section=%s&title=%s&year=%s&img=%s&fanart=%s&pars=%s&labs=%s)' % (sys.argv[0],'FavoritesAdd',section,name,year,labs['thumbnail'],labs['fanart'],pars,labs )))
			### contextMenuItems.append(('Favorites - Add', 'XBMC.RunPlugin(%s?mode=%s&title=%s&year=%s&img=%s&fanart=%s&pars=%s&labs=%s)' % (sys.argv[0],'FavoritesAdd',urllib.quote_plus(name),year,urllib.quote_plus(labs['thumbnail']),urllib.quote_plus(labs['fanart']),pars,labs )))
			### ps('Favorites - '+cFL('Add','green'))
			try: _addon.add_directory(pars, labs, img=labs['thumbnail'], fanart=labs['fanart'], contextmenu_items=contextMenuItems)
			except: 
				uname=name; name='[Unknown]'; _addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
		set_view('movies',ps('setview.movies')); _addon.end_of_directory(); return
	else: return
	_addon.end_of_directory()

def listEpisodes(section, url, img='', season=''): #_param['img']
	xbmcplugin.setContent( int( sys.argv[1] ), 'episodes' ); WhereAmI('@ the Episodes List for TV Show -- url: %s' % url); html=net.http_GET(url).content
	if (html=='') or (html=='none') or (html==None):
		if (_debugging==True): print 'Html is empty.'
		return
	if (img==''):
		match=re.search( 'coverImage">.+?src="(.+?)"', html, re.IGNORECASE | re.MULTILINE | re.DOTALL); img=match.group(1)
	episodes=re.compile('<span class="epname">[\n].+?<a href="(.+?)"[\n]\s+title=".+?">(.+?)</a>[\n]\s+<a href="/.+?/season-(\d+)/episode-(\d+)/" class=".+?">[\n]\s+(\d+) links</a>', re.IGNORECASE | re.MULTILINE | re.DOTALL).findall(html) #; if (_debugging==True): print episodes
	if not episodes: 
		if (_debugging==True): print 'couldn\'t find episodes'
		return
	if (_param['thetvdb_series_id']=='') or (_param['thetvdb_series_id']=='none') or (_param['thetvdb_series_id']==None) or (_param['thetvdb_series_id']==False): thetvdb_episodes=None
	else: thetvdb_episodes=thetvdb_com_episodes2(_param['thetvdb_series_id'])
	#print 'thetvdb_episodes',thetvdb_episodes
	woot=False
	for ep_url, episode_name, season_number, episode_number, num_links in episodes:
		labs={}; s_no=season_number; e_no=episode_number
		if (int(episode_number) > -1) and (int(episode_number) < 10): episode_number='0'+episode_number
		labs['thumbnail']=img; labs['fanart']=_param['fanart']
		labs['EpisodeTitle']=episode_name
		#labs['ShowTitle']=''
		labs['title']=season_number+'x'+episode_number+' - '+episode_name+'  [[I]'+num_links+' Links [/I]]'
		ep_url=_domain_url+ep_url; episode_name=messupText(episode_name,True,True,True,True)
		if (thetvdb_episodes==None) or (_param['thetvdb_series_id']==None) or (_param['thetvdb_series_id']==False) or (_param['thetvdb_series_id'] is not '') or (_param['thetvdb_series_id']=='none'): t=''
		if (thetvdb_episodes):
			#for thetvdb_episode in thetvdb_episodes:
			for db_ep_url, db_sxe_no, db_ep_url2, db_ep_name, db_dateYear, db_dateMonth, db_dateDay, db_hasImage in thetvdb_episodes:
				db_ep_url=ps('meta.tv.domain')+db_ep_url
				db_ep_url2=ps('meta.tv.domain')+db_ep_url2
				### iresults=re.compile('<tr><td class=".+?"><a href="(.+?)">(.+?)</a></td><td class=".+?"><a href="(.+?)">(.+?)</a></td><td class=".+?">(.+?)-(.+?)-(.+?)</td><td class=".+?"><img src="(.+?)" width=.+? height=.+?>.+?</td></tr>').findall(itable)
				### db_ep_url, db_sxe_no, db_epurl2, db_ep_name, db_dateYear, db_dateMonth, db_dateDay, db_hasImage
				if (db_sxe_no.strip()==(s_no+' x '+e_no)):
					if ('Episode #' in episode_name): episode_name=db_ep_name.strip()
					labs['Premeired']=labs['DateAired']=labs['Date']=db_dateYear+'-'+db_dateMonth+'-'+db_dateDay
					labs['year']=db_dateYear; labs['month']=db_dateMonth; labs['day']=db_dateDay
					(db_thumb,labs['thetvdb_series_id'],labs['thetvdb_episode_id']) = Episode__get_thumb(db_ep_url2.strip(),img)
					if (check_ifUrl_isHTML(db_thumb)==True): labs['thumbnail']=db_thumb
					#
					#labs['title']=season_number+'x'+episode_number+' - '+db_ep_name.strip()+'  [[I]'+num_links+' Links [/I]]'
					labs['title']=cFL(season_number+cFL('x',ps('cFL_color4'))+episode_number,ps('cFL_color5'))+' - '+cFL(episode_name,ps('cFL_color4'))+cFL('  [[I]'+cFL(num_links+' Links ',ps('cFL_color3'))+'[/I]]',ps('cFL_color'))
					#cFL('  [[I]'+cFL(num_links+' Links ',ps('cFL_color3'))+'[/I]]',ps('cFL_color'))
					#' - '+db_ep_name.strip()+'  [[I]'+num_links+' Links [/I]]'
					#cFL(season_number+cFL('x',ps('cFL_color4'))+episode_number,ps('cFL_color5'))
					#
					ep_html=mGetItemPage(db_ep_url2); deb('thetvdb - episode - url',db_ep_url2)
					deb('Length of ep_html',str(len(ep_html)))
					if (ep_html is not None) or (ep_html is not False) or (ep_html is not '') or (ep_html is not 'none'):
						labs['PlotOutline']=labs['plot']=mdGetTV(ep_html,['thetvdb.episode.overview1'])['thetvdb.episode.overview1']
						#(ep_html,{'thetvdb.episode.overview'})['thetvdb.episode.overview']
					#if (episode_number=='01'): print ep_html
					#if (woot==False): print ep_html; woot=True
					#
			#
		#
		#
		#
		contextMenuItems=[]; labs['season']=season_number; labs['episode']=episode_number
		##
		##labs['title']=cFL(showTitle+'  ('+cFL(year,ps('cFL_color2'))+')',ps('cFL_color'))
		##if (labs['Country'] is not ''): labs['title']=labs['title']+cFL('  ['+cFL(labs['Country'],ps('cFL_color3'))+']',ps('cFL_color'))
		##labs['title']=labs['title']+'[CR]'
		##if (season_number is not '') and (episode_number is not ''): labs['title']=labs['title']+'  '+cFL(season_number+cFL('x',ps('cFL_color4'))+episode_number,ps('cFL_color5'))
		##if (episode_name is not ''): labs['title']=labs['title']+' - '+cFL(episode_name,ps('cFL_color4'))
		##
		contextMenuItems.append((ps('cMI.showinfo.name'),ps('cMI.showinfo.url')))
		deb('Episode Name',labs['title'])
		deb('episode thumbnail',labs['thumbnail'])
		if (season==season_number) or (season==''): _addon.add_directory({'mode': 'GetLinks', 'year': _param['year'], 'section': section, 'img': img, 'url': ep_url, 'season': season_number, 'episode': episode_number, 'episodetitle': episode_name}, labs, img=labs['thumbnail'], fanart=labs['fanart'], contextmenu_items=contextMenuItems)
	set_view('episodes',ps('setview.episodes')); _addon.end_of_directory()

def listSeasons(section, url, img=''): #_param['img']
	xbmcplugin.setContent(int(sys.argv[1]),'seasons'); WhereAmI('@ the Seasons List for TV Show -- url: %s' % url); html=net.http_GET(url).content
	if (html=='') or (html=='none') or (html==None):
		if (_debugging==True): print 'Html is empty.'
		return
	if (img==''):
		match=re.search(ps('listSeasons.match.img'), html, re.IGNORECASE | re.MULTILINE | re.DOTALL); img=match.group(1)
	##if (_debugging==True): print ParseDescription(html)
	seasons=re.compile(ps('listSeasons.match.seasons')).findall(html)
	if (_debugging==True): print seasons
	if not seasons: 
		if (_debugging==True): print 'couldn\'t find seasons'
		return
	for season_name in seasons:
		season_name=messupText(season_name,False,False,True,True)
		_addon.add_directory({'mode': 'GetEpisodes', 'year': _param['year'], 'section': section, 'img': img, 'url': url, 'season': season_name, 'thetvdb_series_id': _param['thetvdb_series_id'], 'fanart': _param['fanart']}, {'title':  ps('listSeasons.prefix.seasons')+cFL(season_name,ps('cFL_color5'))}, img=img, fanart=_param['fanart'])
	set_view('seasons',ps('setview.seasons')); _addon.end_of_directory()

def Menu_LoadCategories(section=_default_section_): #Categories
	WhereAmI('@ the Category Menu')
	if  ( section == 'tv'): ## TV Show
		##_addon.add_directory({'section': section, 'mode': 'BrowseLatest'},	 		{'title':  'Latest'})
		##_addon.add_directory({'section': section, 'mode': 'BrowsePopular'}, 		{'title':  'Popular'})
		#_addon.add_directory({'section': section, 'mode': 'GetTitlesLatest', 'url': _domain_url+'/tv/', 'pageno': '1','pagecount': '1'}, 		{'title':  'Latest'})
		_addon.add_directory({'section': section, 'mode': 'GetTitlesLatest', 				'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 												{'title':  cFL('L',ps('cFL_color'))+'atest'}, img=_art150,fanart=_artFanart)
		_addon.add_directory({'section': section, 'mode': 'GetTitlesPopular', 			'url': _domain_url+ps('domain.url.tv')+'/', 'pageno': '1','pagecount': '1'}, 		{'title':  cFL('P',ps('cFL_color'))+'opular (ALL TIME)'}, img=_art150,fanart=_artFanart)
		_addon.add_directory({'section': section, 'mode': 'GetTitlesNewPopular', 		'url': _domain_url+ps('domain.url.tv')+'/', 'pageno': '1','pagecount': '1'}, 		{'title':  cFL('P',ps('cFL_color'))+'opular (NEW)'}, img=_art150,fanart=_artFanart)
	else:	#################### Movie
		#_addon.add_directory({'section': section, 'mode': 'GetTitlesLatest', 'url': _domain_url+'/#latest', 'pageno': '1','pagecount': '1'},	 		{'title':  'Latest'})
		##_addon.add_directory({'section': section, 'mode': 'GetTitlesPopular', 'url': _domain_url+'/#popular', 'pageno': '1','pagecount': '1'}, 			{'title':  'Popular'})
		#_addon.add_directory({'section': section, 'mode': 'GetTitlesPopular', 'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 			{'title':  'Popular (ALL TIME)'})
		#_addon.add_directory({'section': section, 'mode': 'GetTitlesLatest', 'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 		{'title':  'Latest'})
		_addon.add_directory({'section': section, 'mode': 'GetTitlesLatest', 				'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 			{'title':  cFL('L',ps('cFL_color'))+'atest'}, img=_art150,fanart=_artFanart)
		_addon.add_directory({'section': section, 'mode': 'GetTitlesNewPopular', 		'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 			{'title':  cFL('P',ps('cFL_color'))+'opular (NEW)'}, img=_art150,fanart=_artFanart)
		_addon.add_directory({'section': section, 'mode': 'GetTitlesHDPopular', 		'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 			{'title':  cFL('P',ps('cFL_color'))+'opular (HD)'}, img=_art150,fanart=_artFanart)
		_addon.add_directory({'section': section, 'mode': 'GetTitlesOtherPopular', 	'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 			{'title':  cFL('P',ps('cFL_color'))+'opular (OTHER)'}, img=_art150,fanart=_artFanart)
	_addon.add_directory({'section': section, 'mode': 'BrowseGenre'},	 				{'title':  cFL('G',ps('cFL_color'))+'enres'}, img=art('genre','.jpg'),fanart=_artFanart)
	_addon.add_directory({'section': section, 'mode': 'BrowseYear'}, 					{'title':  cFL('Y',ps('cFL_color'))+'ear'}, 	img=_art150,fanart=_artFanart)
	_addon.add_directory({'section': section, 'mode': 'Search'},	 						{'title':  cFL('S',ps('cFL_color'))+'earch'}, img=art('icon-search'),fanart=_artFanart)
	_addon.add_directory({'section': section, 'mode': 'FavoritesList'},	 			{'title':  cFL('F',ps('cFL_color'))+'avorites'},img=_art404,fanart=_artFanart)
	_addon.add_directory({'section': section, 'mode': 'FavoritesEmpty'},	 		{'title':  cFL('E',ps('cFL_color'))+'mpty Favorites'},img=art('trash','.gif'),fanart=_artFanart,is_folder=False)
	###_addon.add_directory({'section': section, 'mode': 'BrowseAtoZ'}, 			{'title':  'A-Z'})
	#_addon.add_directory({'section': section, 'mode': 'GetSearchQuery'}, 		{'title':  'Search'})
	###_addon.add_directory({'section': section, 'mode': 'GetTitles'}, 				{'title':  'Favorites'})
	_addon.end_of_directory()
	### http://www.solarmovie.so/latest-movies.html
	### 
	### 
	### 
	### 

def Menu_MainMenu(): #The Main Menu
	WhereAmI('@ the Main Menu')
	_addon.add_directory({'mode': 'LoadCategories', 'section': 'movies'}, {'title':  cFL('M',ps('cFL_color'))+'ovies'},img=art('movies'),fanart=_artFanart)
	_addon.add_directory({'mode': 'LoadCategories', 'section': 'tv'}, 		{'title':  cFL('T',ps('cFL_color'))+'V Shows'},img=art('television'),fanart=_artFanart)
	_addon.add_directory({'mode': 'ResolverSettings'}, {'title':  cFL('R',ps('cFL_color'))+'esolver Settings'},img=art('turtle','.jpg'),is_folder=False,fanart=_artFanart)
	_addon.add_directory({'mode': 'Settings'}, 				 {'title':  cFL('S',ps('cFL_color'))+'ettings'},img=_artSun,is_folder=False,fanart=_artFanart)
	_addon.add_directory({'mode': 'TextBoxFile', 'title': "[COLOR cornflowerblue]Local Change Log:[/COLOR]  %s"  % (__plugin__), 'url': ps('changelog.local')}, {'title': cFL('L',ps('cFL_color'))+'ocal Change Log'},					img=art('thechangelog','.jpg'),is_folder=False,fanart=_artFanart)
	_addon.add_directory({'mode': 'TextBoxUrl',  'title': "[COLOR cornflowerblue]Latest Change Log:[/COLOR]  %s" % (__plugin__), 'url': ps('changelog.url')}, 	{'title': cFL('L',ps('cFL_color'))+'atest Online Change Log'},	img=art('thechangelog','.jpg'),is_folder=False,fanart=_artFanart)
	_addon.add_directory({'mode': 'TextBoxUrl',  'title': "[COLOR cornflowerblue]Latest News:[/COLOR]  %s"       % (__plugin__), 'url': ps('news.url')}, 				{'title': cFL('L',ps('cFL_color'))+'atest Online News'},				img=_art404										,is_folder=False,fanart=_artFanart)
	#
	#
	#
	### ############
	_addon.end_of_directory()
	### ############
	#_addon.show_countdown(9000,'Testing','Working...') ### Time seems to be in seconds.
	#_addon.show_small_popup('Testing','Working...',image=_artSun)
	#sunNote('Test','Working...')
	#

##### /\ ##### Menus #####
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################

def fav__empty(section):
  WhereAmI('@ Favorites - Empty')
  if (debugging==True): print 'fav__empty()'
  saved_favs=cache.get('favs_'+section+'__'); favs=[]; cache.set('favs_'+section+'__', str(favs)); sunNote(bFL('Favorites'),bFL('Your Favorites Have Been Wiped Clean. Bye Bye.'))

def fav__add(section,name,year='',img=_art150,fanart=_artFanart,pars='',labs=''):
	WhereAmI('@ Favorites - Add')
	if (debugging==True): print 'fav__add()',section,name+'  ('+year+')',img,fanart
	saved_favs=cache.get('favs_'+section+'__'); favs=[]; fav_found=False
	if saved_favs:
		if (debugging==True): print saved_favs
		favs=eval(saved_favs)
		if favs:
			if (debugging==True): print favs
			for (_name,_year,_img,_fanart,_country,_url,_plot,_genre,_dbid) in favs:
				if (name==_name) and (year==_year): 
					fav_found=True
					sunNote(bFL(section+':  '+name.upper()+'  ('+year+')'),bFL('Already in your Favorites'))
					return
					#if (fav_found==False): #if (name,year) in favs:
	if   (section==ps('section.tv')):    favs.append((name,year,img,fanart,_param['country'],_param['url'],_param['plot'],_param['genre'],_param['dbid']))
	elif (section==ps('section.movie')): favs.append((name,year,img,fanart,_param['country'],_param['url'],_param['plot'],_param['genre'],''))
	#favs.append((name,year,img,fanart,pars,labs))
	cache.set('favs_'+section+'__', str(favs)); sunNote(bFL(name+'  ('+year+')'),bFL('Added to Favorites'))
	### _addon.add_directory(pars, labs, img=thumbnail, fanart=labs['fanart'], contextmenu_items=contextMenuItems)
	### _artFanart _art150

def fav__list(section):
	WhereAmI('@ Favorites - List - section:  '+section)
	saved_favs=cache.get('favs_'+section+'__'); favs=[];
	if saved_favs:
		#favs=eval(saved_favs)
		if (debugging==True): print saved_favs
		favs=sorted(eval(saved_favs), key=lambda fav: fav[0])
		if favs:
			for (name,year,img,fanart,country,url,plot,genre,dbid) in favs:
				print '----------------------------'
				print name,year,img,fanart,country,url,plot,genre,dbid #,pars,labs
				contextMenuItems=[]; labs2={}; labs2['fanart']=''
				if   (section==ps('section.tv')):
					##### Right Click Menu for: TV #####
					contextMenuItems.append((ps('cMI.showinfo.name'),ps('cMI.showinfo.url')))
					contextMenuItems.append((ps('cMI.airdates.find.name'), 			ps('cMI.airdates.find.url') % (sys.argv[0],ps('cMI.airdates.find.mode'),urllib.quote_plus(name))))
					##### Right Click Menu for: TV ##### /\ #####
					pars2={'mode': 'GetSeasons', 'section': section, 'url': url, 'img': img, 'image': img, 'fanart': fanart, 'title': name, 'year': year, 'thetvdbid': dbid, 'thetvdb_series_id': dbid, 'Country': country, 'plot': plot }
					labs2['ShowTitle']=name; labs2['year']=year
					#labs2['title']=name
					labs2['title']=cFL(name+'  ('+cFL(year,ps('cFL_color2'))+')',ps('cFL_color'))
					if (country is not ''): labs2['title']=labs2['title']+cFL('  ['+cFL(country,ps('cFL_color3'))+']',ps('cFL_color'))
					labs2['image']=img; labs2['fanart']=fanart
					labs2['PlotOutline']=labs2['plot']=plot
					labs2['genre']=genre
					labs2['country']=country
					try: _addon.add_directory(pars2, labs2, img=img, fanart=fanart, contextmenu_items=contextMenuItems)
					except: deb('Error Listing Item',name+'  ('+year+')')
				elif (section==ps('section.movie')):
					##### Right Click Menu for: TV #####
					contextMenuItems.append((ps('cMI.showinfo.name'),ps('cMI.showinfo.url')))
					##### Right Click Menu for: TV ##### /\ #####
					pars2={'mode': 'GetLinks', 'section': section, 'url': url, 'img': img, 'image': img, 'fanart': fanart, 'title': name, 'year': year }
					labs2['ShowTitle']=name; labs2['year']=year
					labs2['title']=cFL(name+'  ('+cFL(year,ps('cFL_color2'))+')',ps('cFL_color'))
					#labs2['title']=cFL(name+'  ('+cFL(year,ps('cFL_color2'))+')  ['+cFL(country,ps('cFL_color3'))+']',ps('cFL_color'))
					labs2['image']=img; labs2['fanart']=fanart
					try: _addon.add_directory(pars2, labs2, img=img, fanart=fanart, contextmenu_items=contextMenuItems)
					except: deb('Error Listing Item',name+'  ('+year+')')
			if   (section==ps('section.tv')): 		set_view('tvshows',ps('setview.tv')			,True)
			elif (section==ps('section.movie')): 	set_view('movies' ,ps('setview.movies')	,True)
		else: 
			sunNote('Favorites:  '+section,'No favorites found *'); return
	else: sunNote('Favorites:  '+section,'No favorites found **'); return
	_addon.end_of_directory()

#	#
#			##### Right Click Menu for: TV #####
#			contextMenuItems.append((ps('cMI.showinfo.name'),ps('cMI.showinfo.url')))
#			if os.path.exists(xbmc.translatePath(ps('special.home.addons'))+ps('cMI.1ch.search.folder')):
#				contextMenuItems.append((ps('cMI.1ch.search.name'), 				ps('cMI.1ch.search.url') 				% (ps('cMI.1ch.search.plugin')			, ps('cMI.1ch.search.section.tv'), name)))
#			if os.path.exists(xbmc.translatePath(ps('special.home.addons'))+ps('cMI.primewire.search.folder')):
#				contextMenuItems.append((ps('cMI.primewire.search.name'), 	ps('cMI.primewire.search.url') 	% (ps('cMI.primewire.search.plugin'), ps('cMI.primewire.search.section.tv'), name)))
#			contextMenuItems.append((ps('cMI.airdates.find.name'), 			ps('cMI.airdates.find.url') % (sys.argv[0],ps('cMI.airdates.find.mode'),urllib.quote_plus(name))))
#			##### Right Click Menu for: TV ##### /\ #####


def fav__remove(section,name,year):
	WhereAmI('@ Favorites - Remove')
	deb('fav__remove()',secction,name+'  ('+year+')'); saved_favs=cache.get('favs_'+section+'__'); tf=False
	if saved_favs:
		favs=eval(saved_favs)
		if favs:
			for (_name,_year,_img,_fanart,_country,_url,_plot,_genre,_dbid) in favs: 
				if (name==_name) and (year==_year):
					favs.remove((_name,_year,_img,_fanart,_country,_url,_plot,_genre,_dbid)); cache.set('favs_'+section+'__', str(favs)); tf=True
					sunNote(bFL(name.upper()+'  ('+year+')'),bFL('Removed from Favorites')); deb(name+'  ('+year+')','Removed from Favorites. (Hopefully)')
					xbmc.executebuiltin("XBMC.Container.Refresh"); return
			if (tf==False): sunNote(bFL(name.upper()),bFL('not found in your Favorites'))
		else: sunNote(bFL(name.upper()+'  ('+year+')'),bFL('not found in your Favorites'))


### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Search #####
def doSearchNormal (section,title=''):
	if (section=='tv'): SearchPrefix=ps('domain.search.tv')
	else: SearchPrefix=ps('domain.search.movie')
	if (title==''):
		title=showkeyboard(txtMessage=title,txtHeader="Title:  ("+section+")")
		if (title=='') or (title=='none') or (title==None) or (title=='False'): return
	_param['url']=SearchPrefix+title
	deb('Searching for',_param['url'])
	listItems(section, _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'])


##### /\ ##### Search #####
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Modes #####
def check_mode(mode=''):
	deb('Mode',mode)
	if (mode=='') or (mode=='main') or (mode=='MainMenu'): 
		initDatabase()
		Menu_MainMenu()
	elif (mode=='ResolverSettings'): urlresolver.display_settings()
	elif (mode=='Settings'): _addon.addon.openSettings() #_plugin.openSettings()
	elif (mode=='PlayVideo'): PlayVideo(_param['url'], _param['infoLabels'], _param['listitem'])
	elif (mode=='LoadCategories'): Menu_LoadCategories(_param['section'])
	#elif (mode=='BrowseAtoZ'): BrowseAtoZ(_param['section'])
	elif (mode=='BrowseYear'): Menu_BrowseByYear(_param['section'])
	elif (mode=='BrowseGenre'): Menu_BrowseByGenre(_param['section'])
	#elif (mode=='BrowseLatest'): BrowseLatest(_param['section'])
	#elif (mode=='BrowsePopular'): BrowsePopular(_param['section'])
	#elif (mode=='GetResults'): GetResults(_param['section'], genre, letter, page)
	elif (mode=='GetTitles'): 						listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'])
	elif (mode=='GetTitlesLatest'): 			listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck=ps('LI.tv.latest.check'))
	elif (mode=='GetTitlesPopular'): 			listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck=ps('LI.tv.popular.all.check'))
	elif (mode=='GetTitlesHDPopular'): 		listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck=ps('LI.movies.popular.hd.check'))
	elif (mode=='GetTitlesOtherPopular'): listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck=ps('LI.movies.popular.other.check'))
	elif (mode=='GetTitlesNewPopular'): 	listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck=ps('LI.movies.popular.new.check'))
	elif (mode=='GetLinks'): listLinks(_param['section'], _param['url'], showtitle=_param['showtitle'], showyear=_param['showyear'])
	elif (mode=='GetSeasons'): listSeasons(_param['section'], _param['url'], _param['img'])
	elif (mode=='GetEpisodes'): listEpisodes(_param['section'], _param['url'], _param['img'], _param['season'])
	elif (mode=='TextBoxFile'): TextBox2().load_file(_param['url'],_param['title'])
	elif (mode=='TextBoxUrl'):  TextBox2().load_url( _param['url'],_param['title'])
	elif (mode=='SearchForAirDates'):  search_for_airdates(_param['title'])
	elif (mode=='Search'):  doSearchNormal(_param['section'],_param['title'])
	elif (mode=='FavoritesList'):  		  fav__list(_param['section'])
	elif (mode=='FavoritesEmpty'):  	 fav__empty(_param['section'])
	elif (mode=='FavoritesRemove'):  	fav__remove(_param['section'],_param['title'],_param['year'])
	elif (mode=='FavoritesAdd'):  		   fav__add(_param['section'],_param['title'],_param['year'],_param['img'],_param['fanart'],_param['pars'],_param['labs'])
	#elif (mode=='favoritesadd'):  		   fav__add(_param['section'],_param['title'],_param['year'],_param['img'],_param['fanart'],_param['pars'],_param['labs'])
	#elif (mode=='GetSearchQuery'): GetSearchQuery(_param['section'])
	#elif (mode=='Search'): Search(_param['section'], query)
##### /\ ##### Modes #####
### ############################################################################################################
deb('param >> title',_param['title'])
deb('param >> url',_param['url']) ### Simply Logging the current query-passed / param -- URL
check_mode(_param['mode']) ### Runs the function that checks the mode and decides what the plugin should do. This should be at or near the end of the file.
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
