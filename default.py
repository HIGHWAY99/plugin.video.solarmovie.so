### ############################################################################################################
###	#	
### # Project: 			#		SolarMovie.so - by The Highway 2013.
### # Author: 			#		The Highway
### # Version:			#		v0.1.3
### # Description: 	#		http://www.solarmovie.so
###	#	
### ############################################################################################################
### ############################################################################################################
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs,urlresolver,urllib,urllib2,re,os,sys,htmllib,string,StringIO,logging,random,array,time,datetime,unicodedata,requests
#import zipfile

from t0mm0.common.addon import Addon
from t0mm0.common.net 	import Net
### 
import HTMLParser, htmlentitydefs
try: from script.module.metahandler import metahandlers
except: from metahandler import metahandlers
try:
	from sqlite3 		import dbapi2 as sqlite
	print "Loading sqlite3 as DB engine"
except:
	from pysqlite2 	import dbapi2 as sqlite
	print "Loading pysqlite2 as DB engine"
### 
try: import StorageServer
except: import storageserverdummy as StorageServer
from teh_tools import *
#from menus import *
#from globals import *




### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
__plugin__	="[COLOR yellow]S[/COLOR]olarmovie.so"
__authors__	="[COLOR white]The[COLOR tan]Highway[/COLOR][/COLOR]"
__credits__	="anilkuj of plugin.video.soloremovie (solarmovie.eu) for much initial work, TheHighway of plugin.video.theanimehighway for teh_tools.py"
_addon_id		="plugin.video.solarmovie.so"
_domain_url ="http://www.solarmovie.so"
_database_file=os.path.join(xbmc.translatePath("special://database"), 'solarmovieso.db')
_plugin_id	=_addon_id
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
_addon=Addon(_addon_id, sys.argv); _plugin=xbmcaddon.Addon(id=_addon_id) #; _plug=xbmcplugin
addon=_addon
### 
_addonPath=xbmc.translatePath(_plugin.getAddonInfo('path'))
_artPath=xbmc.translatePath(os.path.join(_addonPath,'art'))
_artIcon		=_addon.get_icon()
_artFanart	=_addon.get_fanart()
_artSun			=xbmc.translatePath(os.path.join(_artPath,'sun.png'))
_datapath = addon.get_profile()
### 
if _addon.get_setting("debug-enable") == "true":			_debugging=True				#if (_debugging==True): 
else: 																								_debugging=False
if _addon.get_setting("debug-show") == "true":				_shoDebugging=True		#if (_showDebugging==True): 
else: 																								_shoDebugging=False
if _addon.get_setting("enableMeta") == "true":				_enableMeta=True		#if (_showDebugging==True): 
else: 																								_enableMeta=False
### 
if (_debugging==True): print 'Addon Path: '+_addonPath
if (_debugging==True): print 'Art Path: '+_artPath
if (_debugging==True): print 'Addon Icon Path: '+_artIcon
if (_debugging==True): print 'Addon Fanart Path: '+_artFanart
### 
_setting={}; _param={}
### ############################################################################################################


net=Net()
DB=_database_file; BASE_URL=_domain_url;

### ############################################################################################################
GENRES = ['Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western']
_default_section_='movies'


### ############################################################################################################
##### Queries ##########
_setting['debug-enable']=_addon.get_setting("debug-enable") #_setting['debug-enable']=_plugin.getSetting("debug-enable")
_setting['debug-show']=_addon.get_setting("debug-show") 		#_setting['debug-show']=_plugin.getSetting("debug-show")
_setting['enableMeta']=_addon.get_setting("enableMeta")
_param['mode']=_addon.queries.get('mode','')
_param['url']=_addon.queries.get('url','')
_param['pagesource']=_addon.queries.get('pagesource','')
_param['pageurl']=_addon.queries.get('pageurl','')
_param['pageno']=_addon.queries.get('pageno',0)
_param['pagecount']=_addon.queries.get('pagecount',1)
#_param['pagestart']=_addon.queries.get('pagestart',0)
_param['fanart']=_addon.queries.get('fanart','')
_param['img']=_addon.queries.get('img','')
_param['thumbnail']=_addon.queries.get('thumbnail','')
_param['thumbnail']=_addon.queries.get('thumbnailshow','')
_param['thumbnail']=_addon.queries.get('thumbnailepisode','')
_param['section']=_addon.queries.get('section','movies')
_param['by']=_addon.queries.get('by','')
_param['letter']=_addon.queries.get('letter','')
_param['year']=_addon.queries.get('year','')
_param['genre']=_addon.queries.get('genre','')
_param['title']=_addon.queries.get('title','')
_param['showtitle']=_addon.queries.get('showtitle','')
_param['showyear']=_addon.queries.get('showyear','')
_param['listitem']=_addon.queries.get('listitem','')
_param['infoLabels']=_addon.queries.get('infoLabels','')
_param['season']=_addon.queries.get('season','')
_param['episode']=_addon.queries.get('episode','')
#_param['']=_addon.queries.get('','')
#_param['']=_addon.queries.get('','')
#_param['']=_addon.queries.get('','')
#_param['']=_addon.queries.get('','')

#mode = addon.queries['mode']
#url = addon.queries.get('url', None)
#section = addon.queries.get('section', None)
#img = addon.queries.get('img', None)
#genre = addon.queries.get('genre', None)
#year = addon.queries.get('year', None)
#letter = addon.queries.get('letter', None)
#page = addon.queries.get('page', None)
#episodes = addon.queries.get('episodes', None)
#listitem = addon.queries.get('listitem', None)
#query = addon.queries.get('query', None)
#startPage = addon.queries.get('startPage', None)
#numOfPages = addon.queries.get('numOfPages', None)

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
def PlayVideo(url, infoLabels, listitem):
	My_infoLabels=eval(infoLabels)
	#My_infoLabels={ "Title": ShowTitle, "Year": ShowYear, "Plot": ShowPlot, 'IMDbURL': IMDbURL, 'IMDbID': IMDbID, 'IMDb': IMDbID }
	infoLabels={ "Studio": My_infoLabels['Studio'], "ShowTitle": My_infoLabels['ShowTitle'], "Title": My_infoLabels['Title'], "Year": My_infoLabels['Year'], "Plot": My_infoLabels['Plot'], 'IMDbURL': My_infoLabels['IMDbURL'], 'IMDbID': My_infoLabels['IMDbID'], 'IMDb': My_infoLabels['IMDb'] }
	#
	#li=xbmcgui.ListItem()
	li=xbmcgui.ListItem(_param['title'], iconImage=_param['img'], thumbnailImage=_param['img'])
	WhereAmI('@ PlayVideo -- Getting ID From:  %s' % url)
	match = re.search( '/.+?/.+?/(.+?)/', url) ## http://www.solarmovie.so/link/show/1052387/ ##
	videoId = match.group(1)
	deb('Solar ID',videoId)
	url = BASE_URL + '/link/play/' + videoId + '/' ## http://www.solarmovie.so/link/play/1052387/ ##
	html = net.http_GET(url).content
	match = re.search( '<iframe.+?src="(.+?)"', html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
	link = match.group(1)
	link = link.replace('/embed/', '/file/')
	deb('hoster link',link)
	if (_debugging==True): print listitem
	if (_debugging==True): print infoLabels
	#xbmc.Player( xbmc.PLAYER_CORE_PAPLAYER ).play(stream_url, li)
	#infoLabels.append('url': stream_url)
	li.setInfo(type="Video", infoLabels=infoLabels )
	li.setProperty('IsPlayable', 'true')
	#if (urlresolver.HostedMediaFile(link).valid_url()):
	#else: 
	try: stream_url = urlresolver.HostedMediaFile(link).resolve()
	except: 
		if (_debugging==True): print 'Link URL Was Not Resolved: '+link
		notification("urlresolver.HostedMediaFile(link).resolve()","Failed to Resolve Playable URL.")
		return
	#stream_url = urlresolver.HostedMediaFile(url=link).resolve()
	#deb('Stream Url',stream_url)
	#listitem.setPath(stream_url)
	#xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
	#xbmc.sleep(1000)
	_addon.end_of_directory()
	#xbmc.Player().stop()
	play=xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	play.play(stream_url, li)
	xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)
	#play.add(stream_url, li)
	#xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(stream_url, li)
	#xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(stream_url)#, li)
	#xbmc.sleep(7000)
	#_addon.add_video_item({'infoLabels': My_infoLabels}, {'title':  'Play'}, url=stream_url)
	#_addon.end_of_directory()
	### xbmc.PLAYER_CORE_AUTO | xbmc.PLAYER_CORE_DVDPLAYER | xbmc.PLAYER_CORE_MPLAYER | xbmc.PLAYER_CORE_PAPLAYER
	#xbmc.Player( xbmc.PLAYER_CORE_AUTO ).play(LK[rSelect]['VideoUrl'], listitem)#, windowed)
	#xbmc.Player().play(stream_url, listitem)
        
def PlayTrailer(url):
	url = url.decode('base-64')
	WhereAmI('@ PlayVideo:  %s' % url)
	sources = []
	try: 
		hosted_media = urlresolver.HostedMediaFile(url=url)
		sources.append(hosted_media)
		source = urlresolver.choose_source(sources)
		if source: stream_url = source.resolve()
	except:
		deb('Stream failed to resolve',url)
		return
	else: stream_url = ''
	try: xbmc.Player().play(stream_url)
	except: 
		deb('Video failed to play',stream_url)
		return

### ############################################################################################################
### ############################################################################################################
### ############################################################################################################

def art(f,fe='.png'):
	return xbmc.translatePath(os.path.join(_artPath,f+fe))
	
def WhereAmI(t):
	if (_debugging==True): print 'Where am I:  '+t

def deb(s,t):
	if (_debugging==True): print s+':  '+t

def Menu_MainMenu(): #homescreen
	WhereAmI('@ the Main Menu')
	clrFirstLetter='goldenrod'
	_addon.add_directory({'mode': 'LoadCategories', 'section': 'movies'}, {'title':  '[COLOR '+clrFirstLetter+']M[/COLOR]ovies'},img=art('movies'))
	_addon.add_directory({'mode': 'LoadCategories', 'section': 'tv'}, 		{'title':  '[COLOR '+clrFirstLetter+']T[/COLOR]V Shows'},img=art('television'))
	_addon.add_directory({'mode': 'ResolverSettings'}, {'title':  '[COLOR '+clrFirstLetter+']R[/COLOR]esolver Settings'},is_folder=False)
	_addon.add_directory({'mode': 'Settings'}, 				 {'title':  '[COLOR '+clrFirstLetter+']S[/COLOR]ettings'},img=_artSun,is_folder=False)
	_addon.add_directory({'mode': 'TextBoxFile', 'title': "[COLOR cornflowerblue]Local Change Log:[/COLOR]  %s"  % (__plugin__), 'url': 'changelog.txt'}, 				 																																 {'title': '[COLOR white]Local[/COLOR] [COLOR tan]Change Log[/COLOR]'},					img=_artSun,is_folder=False)
	_addon.add_directory({'mode': 'TextBoxUrl',  'title': "[COLOR cornflowerblue]Latest Change Log:[/COLOR]  %s" % (__plugin__), 'url': 'https://raw.github.com/HIGHWAY99/plugin.video.solarmovie.so/master/changelog.txt'}, 		 {'title': '[COLOR white]Latest Online[/COLOR] [COLOR tan]Change Log[/COLOR]'},	img=_artSun,is_folder=False)
	_addon.add_directory({'mode': 'TextBoxUrl',  'title': "[COLOR cornflowerblue]Latest News:[/COLOR]  %s"       % (__plugin__), 'url': 'https://raw.github.com/HIGHWAY99/plugin.video.solarmovie.so/master/news.txt'}, 				 {'title': '[COLOR white]Latest Online[/COLOR] [COLOR tan]News[/COLOR]'},				img=_artSun,is_folder=False)
	##_addon.add_directory({'mode': 'TextBox'}, 				 {'title':  '[COLOR white]Local[/COLOR] [COLOR tan]Change Log[/COLOR]'},img=_artSun,is_folder=False)
	##_addon.add_directory({'mode': 'TextBox'}, 				 {'title':  '[COLOR white]Local[/COLOR] [COLOR tan]Change Log[/COLOR]'},img=_artSun,is_folder=False)
	### ############
	_addon.end_of_directory()
	### _plug.endOfDirectory(int(sys.argv[1]))
	### xbmcplugin.endOfDirectory(int(sys.argv[1]))
	### ############

def Menu_LoadCategories(section=_default_section_): #Categories
	WhereAmI('@ the Category Menu')
	if  ( section == 'tv'): ## TV Show
		##_addon.add_directory({'section': section, 'mode': 'BrowseLatest'},	 		{'title':  'Latest'})
		##_addon.add_directory({'section': section, 'mode': 'BrowsePopular'}, 		{'title':  'Popular'})
		#_addon.add_directory({'section': section, 'mode': 'GetTitlesLatest', 'url': _domain_url+'/tv/', 'pageno': '1','pagecount': '1'}, 		{'title':  'Latest'})
		_addon.add_directory({'section': section, 'mode': 'GetTitlesPopular', 'url': _domain_url+'/tv/', 'pageno': '1','pagecount': '1'}, 		{'title':  'Popular (ALL TIME)'})
		_addon.add_directory({'section': section, 'mode': 'GetTitlesNewPopular', 'url': _domain_url+'/tv/', 'pageno': '1','pagecount': '1'}, 	{'title':  'Popular (NEW)'})
	else:	#################### Movie
		#_addon.add_directory({'section': section, 'mode': 'GetTitlesLatest', 'url': _domain_url+'/#latest', 'pageno': '1','pagecount': '1'},	 		{'title':  'Latest'})
		##_addon.add_directory({'section': section, 'mode': 'GetTitlesPopular', 'url': _domain_url+'/#popular', 'pageno': '1','pagecount': '1'}, 			{'title':  'Popular'})
		#_addon.add_directory({'section': section, 'mode': 'GetTitlesPopular', 'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 			{'title':  'Popular (ALL TIME)'})
		#_addon.add_directory({'section': section, 'mode': 'GetTitlesLatest', 'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 		{'title':  'Latest'})
		_addon.add_directory({'section': section, 'mode': 'GetTitlesNewPopular', 'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 	{'title':  'Popular (NEW)'})
		_addon.add_directory({'section': section, 'mode': 'GetTitlesHDPopular', 'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 			{'title':  'Popular (HD)'})
		_addon.add_directory({'section': section, 'mode': 'GetTitlesOtherPopular', 'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 			{'title':  'Popular (OTHER)'})
	_addon.add_directory({'section': section, 'mode': 'BrowseGenre'},	 			{'title':  'Genres'})
	_addon.add_directory({'section': section, 'mode': 'BrowseYear'}, 				{'title':  'Year'})
	###_addon.add_directory({'section': section, 'mode': 'BrowseAtoZ'}, 			{'title':  'A-Z'})
	#_addon.add_directory({'section': section, 'mode': 'GetSearchQuery'}, 		{'title':  'Search'})
	###_addon.add_directory({'section': section, 'mode': 'GetTitles'}, 				{'title':  'Favorites'})
	_addon.end_of_directory()
	### http://www.solarmovie.so/latest-movies.html
	### 
	### 
	### 
	### 
	### 
	### 
	### 
	### 
	### 
	### 
	### 
	### 

def Menu_BrowseByGenre(section=_default_section_):
	url=''; WhereAmI('@ the Genre Menu')#print 'Browse by genres screen'
	for genre in GENRES:
		if section == 'movies': url=_domain_url+'/watch-'   +(genre.lower())+  '-movies.html'
		else: 									url=_domain_url+'/tv/watch-'+(genre.lower())+'-tv-shows.html'
		addon.add_directory({'section': section,'mode': 'GetTitles','url': url,'genre': genre,'pageno': '1','pagecount': '3'}, {'title':  genre})
		### addon.add_directory({'section': section, 'mode': 'GetTitles', 'url': url, 'year': year, 'startPage': '1', 'numOfPages': '3'}, {'title':  genre})
	_addon.end_of_directory()

def Menu_BrowseByYear(section=_default_section_):
	url=''; WhereAmI('@ the Year Menu')#print 'Browse by year screen'
	EarliestYear=1929 #1930 ### This is set to 1 year earlier so that it will display too ### 
	try: thisyear=int(datetime.date.today().strftime("%Y"))
	except: thisyear=2013
	for year in range(thisyear, EarliestYear, -1):
		if section == 'movies': url=_domain_url+   '/watch-movies-of-'+str(year)+'.html'
		else: 									url=_domain_url+'/tv/watch-tv-shows-' +str(year)+'.html'
		addon.add_directory({'section': section,'mode': 'GetTitles', 'url': url,'year': year,'pageno': '1','pagecount': '3'}, {'title':  str(year)})
	_addon.end_of_directory()

def nolines(t):
	it=t.splitlines()
	t=''
	for L in it:
		t=t+L
	t=((t.replace("\r","")).replace("\n",""))
	return t

def netURL(url):
	return net.http_GET(url).content

def remove_accents(input_str):
	nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
	return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def listLinks(section, url, showtitle='', showyear=''):
	WhereAmI('@ the Link List: %s' % url); sources=[]; listitem=xbmcgui.ListItem()
	if (url==''): return
	html=net.http_GET(url).content
	html=html.encode("ascii", "ignore")
	#if (_debugging==True): print html
	if  ( section == 'tv'): ## TV Show
		match=re.compile('<title>Watch (.+?) Online for Free - (.+?) - .+? - (\d+)x(\d+) - SolarMovie</title>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]
		### <title>Watch The Walking Dead Online for Free - Prey - S03E14 - 3x14 - SolarMovie</title>
		if (_debugging==True): print match
		if (match==None): return
		#ShowYear=showyear
		ShowYear=_param['year']
		ShowTitle=match[0].strip(); EpisodeTitle=match[1].strip(); Season=match[2].strip(); Episode=match[3].strip()
		ShowTitle=HTMLParser.HTMLParser().unescape(ShowTitle); ShowTitle=ParseDescription(ShowTitle); ShowTitle=ShowTitle.encode('ascii', 'ignore'); ShowTitle=ShowTitle.decode('iso-8859-1')
		EpisodeTitle=HTMLParser.HTMLParser().unescape(EpisodeTitle); EpisodeTitle=ParseDescription(EpisodeTitle); EpisodeTitle=EpisodeTitle.encode('ascii', 'ignore'); EpisodeTitle=EpisodeTitle.decode('iso-8859-1')
		if ('<p id="plot_' in html):
			ShowPlot=(re.compile('<p id="plot_\d+">(.+?)</p>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
			ShowPlot=HTMLParser.HTMLParser().unescape(ShowPlot); ShowPlot=ParseDescription(ShowPlot); ShowPlot=ShowPlot.encode('ascii', 'ignore'); ShowPlot=ShowPlot.decode('iso-8859-1')
		else: ShowPlot=''
		match=re.compile('<strong>IMDb ID:</strong>[\n]\s+<a href="(.+?)">(\d+)</a>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]
		if (_debugging==True): print match
		(IMDbURL,IMDbID)=match
		IMDbURL=IMDbURL.strip(); IMDbID=IMDbID.strip()
		#
		My_infoLabels={ "Studio": ShowTitle+'  ('+ShowYear+'):  '+Season+'x'+Episode+' - '+EpisodeTitle, "Title": ShowTitle, "ShowTitle": ShowTitle, "Year": ShowYear, "Plot": ShowPlot, 'Season': Season, 'Episode': Episode, 'EpisodeTitle': EpisodeTitle, 'IMDbURL': IMDbURL, 'IMDbID': IMDbID, 'IMDb': IMDbID }
		listitem.setInfo(type="Video", infoLabels=My_infoLabels )
		#
		#
		#match=re.search('bradcramp.+?href=".+?>(.+?)<.+?href=".+?>        Season (.+?) .+?[&nbsp;]+Episode (.+?)<', html, re.MULTILINE | re.IGNORECASE | re.DOTALL)
		#if (_debugging==True): print match
		#if (match==None): return
		#listitem.setInfo('video', {'TVShowTitle': match.group(1), 'Season': int(match.group(2)), 'Episode': int(match.group(3)) } )
	else:	#################### Movie
		#match=re.search('float:left;">(.+?)<em.+?html">[\n]*(.+?)</a>', html, re.MULTILINE | re.IGNORECASE | re.DOTALL)
		#<title>Watch Full The Dark Knight (2008)  Movie Online - Page 1 - SolarMovie</title>
		#match=re.search('<title>Watch Full (.+?) \((.+?)\) .+?</title>', html, re.MULTILINE | re.IGNORECASE | re.DOTALL)
		match=re.compile('<title>Watch Full (.+?) \((.+?)\) .+?</title>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]
		if (_debugging==True): print match
		if (match==None): return
		ShowYear=match[1].strip(); ShowTitle=match[0].strip()
		ShowTitle=HTMLParser.HTMLParser().unescape(ShowTitle); ShowTitle=ParseDescription(ShowTitle); ShowTitle=ShowTitle.encode('ascii', 'ignore'); ShowTitle=ShowTitle.decode('iso-8859-1')
		#
		ShowPlot=(re.compile('<p id="plot_\d+">(.+?)</p>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
		ShowPlot=HTMLParser.HTMLParser().unescape(ShowPlot); ShowPlot=ParseDescription(ShowPlot); ShowPlot=ShowPlot.encode('ascii', 'ignore'); ShowPlot=ShowPlot.decode('iso-8859-1')
		#
		match=re.compile('<strong>IMDb ID:</strong>[\n]\s+<a href="(.+?)">(\d+)</a>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]
		if (_debugging==True): print match
		(IMDbURL,IMDbID)=match
		IMDbURL=IMDbURL.strip(); IMDbID=IMDbID.strip()
		#
		My_infoLabels={ "Studio": ShowTitle+'  ('+ShowYear+')', "Title": ShowTitle, "ShowTitle": ShowTitle, "Year": ShowYear, "Plot": ShowPlot, 'IMDbURL': IMDbURL, 'IMDbID': IMDbID, 'IMDb': IMDbID }
		##liz.setInfo( type="Video", infoLabels={ "Title": showtitle, "Studio": Studio } )
		listitem.setInfo(type="Video", infoLabels=My_infoLabels )
		#listitem.setInfo('video', {'Title': match.group(1).strip(), 'Year': int(match.group(2).strip())} )
	#
	match =  re.compile('<tr id=.+?href="(.+?)">(.+?)<.+?class="qualityCell">(.+?)<.+?<td class="ageCell .+?">(.+?)</td>', re.MULTILINE | re.DOTALL | re.IGNORECASE).findall(html)
	#match =  re.compile('<tr id=.+?href="(.+?)">(.+?)<.+?class="qualityCell">(.+?)<', re.MULTILINE | re.DOTALL | re.IGNORECASE).findall(html)
	### print ' length of match is %d' % len(match)
	if (len(match) > 0):
		count=1
		for url, host, quality, age in match:
			host=host.strip(); quality=quality.strip(); name=str(count)+". "+host+' - [[B]'+quality+'[/B]] - ([I]'+age+'[/I])'
			if urlresolver.HostedMediaFile(host=host, media_id='xxx'):
				img='http://www.google.com/s2/favicons?domain='+host
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
	else:
		return

##def listItems(section=_default_section_, url='', html='', episode=False, startPage='1', numOfPages='1', genre='', year='', stitle=''): # List: Movies or TV Shows
def listItems(section=_default_section_, url='', startPage='1', numOfPages='1', genre='', year='', stitle='', season='', episode='', html='', chck=''): # List: Movies or TV Shows
	if (url==''): return
	if (chck=='Latest'): url=url+chr(35)+'latest'
	WhereAmI('@ the Item List -- url: %s' % url)
	start=int(startPage); end=(start+int(numOfPages)); html=''; html_last=''; nextpage=startPage
	last=2
	try: html_=net.http_GET(url).content
	except: 
		try: html_=getURL(url)
		except: 
			try: html_=getURLr(url,_domain_url)
			except: html_=''
	#print html_
	if (html_=='') or (html_=='none') or (html_==None): return
	pmatch=re.findall('<li><a href=.+?page=([\d]+)"', html_)
	if pmatch: last=pmatch[-1]
	for page in range(start,min(last,end)):
		if (int(startPage)> 1): pageUrl=url+'?page='+startPage
		else: pageUrl=url
		try: 
			##html_last=getURL(pageUrl)
			try: html_last=net.http_GET(pageUrl).content
			except: 
				try: html_=getURL(url)
				except: t=''
			if (_shoDebugging==True) and (html_last==''): notification('Testing','html_last is empty')
			###html=html+(html_last.split('<div class="searchResult">')[1]).split('<hr />')[0] ### Stripping away the surrounding data around the Movie/TV-Show Items.
			if (html_last in html): t=''
			else: html=html+'\r\n'+html_last
			#html=html+'\r\n'+nolines((html_last.split('<div class="searchResult">')[1]).split('<div id="sidebar">')[0]) ### Stripping away the surrounding data around the Movie/TV-Show Items.
			##if (_debugging==True): print html_last
		except: t=''
	if ('<li class="next"><a href="http://www.solarmovie.so/' in html_last): 
		if (_debugging==True): print 'A next-page has been found.'
		#nextpage=re.compile('<li class="next"><a href="http://www.solarmovie.so/.+?.html?page=(\d+)"></a></li>').findall(html_last)[0]
		nextpage=re.findall('<li class="next"><a href=.+?page=([\d]+)"', html_last)[0]
		if (int(nextpage) > end) or (end < last): ## Do Show Next Page Link ##
			if (_debugging==True): print 'A next-page is being added.'
			_addon.add_directory({'mode': 'GetTitles', 'url': url, 'pageno': nextpage, 'pagecount': numOfPages}, {'title': '  >  Next...'}, img=art('icon-next'))
	##	### _addon.add_directory({'mode': 'GetTitles', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': 'Next...'})
	##html=net.http_GET(url).content
	##html=netURL(url).content
	##html=getURL(url)
	##html=nolines(html)
	html=ParseDescription(html)
	html=remove_accents(html)
	#if (_debugging==True): print html
	if   (section=='tv') and (season=='') and (episode==''): ## TV Show
		deb('listItems >> ',section)
		deb('listItems >> chck',chck)
		if   (chck=='NewPopular'):
			print html
			html=(html.split('<h2>Most Popular New TV Shows</h2>')[1]).split('<h3>')[0]
		elif (chck=='Popular'):
			html=(html.split('<h2>Most Popular TV Shows</h2>')[1]).split('<h2>')[0]
		iitems=re.compile('class="coverImage" title="(.+?)".+?href="(.+?)".+?src="(.+?)".+?<a title=".+?\(([\d]+)\)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)
		for name, item_url, thumbnail, year in iitems:
			name=ParseDescription(HTMLParser.HTMLParser().unescape(name))
			#name = remove_accents(name)
			name=name.encode('ascii', 'ignore')
			name=name.decode('iso-8859-1')
			name=name.strip()
			try: deb('listItems >> '+section+' >> '+name, item_url)
			except: print item_url
			contextMenuItems=[]
			contextMenuItems.append(('Show Information', 			'XBMC.Action(Info)'))
			if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.1channel'):
				contextMenuItems.append(('Search 1Channel', 			'XBMC.Container.Update(%s?mode=7000&section=%s&query=%s)' % ('plugin://plugin.video.1channel/', 'tv-shows', name)))
			if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.primewire'):
				contextMenuItems.append(('Search PrimeWire.ag', 	'XBMC.Container.Update(%s?mode=7000&section=%s&query=%s)' % ('plugin://plugin.video.primewire/', 'tv-shows', name)))
			contextMenuItems.append(('Find AirDates', 			'XBMC.RunPlugin(%s?mode=%s&title=%s)' % (sys.argv[0],'SearchForAirDates', urllib.quote_plus(name))))
			#
			if (_enableMeta==True):
				metaget=metahandlers.MetaData()
				meta=metaget.get_meta('tvshow', name, year=year)
				if (meta['imdb_id']=='') and (meta['tvdb_id']==''):
					meta=metaget.get_meta('tvshow', name)
					#try: 
					_addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': meta['cover_url'], 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=meta['cover_url'], fanart=meta['backdrop_url'], contextmenu_items=contextMenuItems)
					#except: 
					#	uname=name
					#	name='[Unknown]'
					#	try: _addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': meta['cover_url'], 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=meta['cover_url'], fanart=meta['backdrop_url'], contextmenu_items=contextMenuItems)
					#	except: _addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail)
				else:
					#try: 
					_addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
					#except: 
					#	uname=name
					#	name='[Unknown]'
					#	_addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail)
			else:
				try: _addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
				except: 
					uname=name
					name='[Unknown]'
					_addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
		set_view('tvshows',515,True)
		_addon.end_of_directory()
	elif (section=='tv') and (episode==''): ## Season
		set_view('seasons',515)
		_addon.end_of_directory()
	elif (section=='tv'): ## Episode
		set_view('episodes',515)
		_addon.end_of_directory()
	elif (section=='movies') or (section=='movie'): ## Movie
		deb('listItems >> ',section)
		deb('listItems >> chck',chck)
		if   (chck=='NewPopular'):
			html=(html.split('<h2>Most Popular New Movies</h2>')[1]).split('<h2>')[0]
		elif (chck=='HDPopular'):
			html=(html.split('<h2>Most Popular Movies in HD</h2>')[1]).split('<h2>')[0]
		elif (chck=='OtherPopular'):
			html=(html.split('<h2>Other Popular Movies</h2>')[1]).split('<h3>')[0]
		#elif (chck=='Popular'): ## I guess this isnt used for movies atm.
		#	match=re.compile('<h2>Most Popular TV Shows</h2>(.+?)<h2>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]
		#	html=match[0]
		#	#html=html.split('<h2>Most Popular TV Shows</h2>')[1]
		#	#html=html.split('<h2>')[0]
		iitems=re.compile('class="coverImage" title="(.+?)".+?href="(.+?)".+?src="(.+?)".+?<a title=".+?\(([\d]+)\)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)
		for name, item_url, thumbnail, year in iitems:
			name = ParseDescription(HTMLParser.HTMLParser().unescape(name))
			#name = remove_accents(name)
			name=name.encode('ascii', 'ignore')
			name=name.decode('iso-8859-1')
			try: deb('listItems >> '+section+' >> '+name, item_url)
			except: print item_url
			contextMenuItems=[]
			contextMenuItems.append(('Show Information', 			'XBMC.Action(Info)'))
			if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.1channel'):
				contextMenuItems.append(('Search 1Channel', 			'XBMC.Container.Update(%s?mode=7000&section=%s&query=%s)' % ('plugin://plugin.video.1channel/', 'movies', name)))
			if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.primewire'):
				contextMenuItems.append(('Search PrimeWire.ag', 	'XBMC.Container.Update(%s?mode=7000&section=%s&query=%s)' % ('plugin://plugin.video.primewire/', 'movies', name)))
			try: _addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
			except: 
				uname=name
				name='[Unknown]'
				_addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
		set_view('movies',515)
		_addon.end_of_directory()
	else: return
	#
	#
	#thumbnail='http://static.solarmovie.so/images/'+(img)+'.jpg'
	#
	#re.compile('(.+?)').findall(link)
	#
	#
	#
	#
	#<li class="next"><a href="http://www.solarmovie.so/watch-action-movies.html?page=2"></a></li>
	#
	#
	#
	#
	#
	_addon.end_of_directory()
	
def listEpisodes(section, url, img='', season=''): #_param['img']
	xbmcplugin.setContent( int( sys.argv[1] ), 'episodes' )
	WhereAmI('@ the Episodes List for TV Show -- url: %s' % url)
	html = net.http_GET(url).content
	if (html=='') or (html=='none') or (html==None):
		if (_debugging==True): print 'Html is empty.'
		return
	if (img==''):
		match=re.search( 'coverImage">.+?src="(.+?)"', html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
		img=match.group(1)
	episodes=re.compile('<span class="epname">[\n].+?<a href="(.+?)"[\n]\s+title=".+?">(.+?)</a>[\n]\s+<a href="/.+?/season-(\d+)/episode-(\d+)/" class=".+?">[\n]\s+(\d+) links</a>', re.IGNORECASE | re.MULTILINE | re.DOTALL).findall(html)
	#episodes=re.compile('<span class="epname">[\n].+?<a href="(.+?)"[\n]\s+title=".+?">(.+?)</a>[\n]\s+[\n]\s+<a href="/.+?/season-(\d+)/episode-(\d+)/" class=".+?">[\n]\s+(\d+) links</a>', re.IGNORECASE | re.MULTILINE | re.DOTALL).findall(html)
	#if (_debugging==True): print episodes
	if not episodes: 
		if (_debugging==True): print 'couldn\'t find episodes'
		return
	for ep_url, episode_name, season_number, episode_number, num_links in episodes:
		if (int(episode_number) > -1) and (int(episode_number) < 10): episode_number='0'+episode_number
		ep_url=_domain_url+ep_url
		episode_name=ParseDescription(HTMLParser.HTMLParser().unescape(episode_name))
		episode_name=episode_name.encode('ascii', 'ignore')
		episode_name=episode_name.decode('iso-8859-1')
		episode_name=episode_name.replace( '_',' ')
		if (season==season_number) or (season==''): 
			addon.add_directory({'mode': 'GetLinks', 'year': _param['year'], 'section': section, 'img': img, 'url': ep_url, 'season': season_number, 'episode': episode_number, 'episodetitle': episode_name}, {'title':  season_number+'x'+episode_number+' - '+episode_name+'  [[I]'+num_links+' Links [/I]]'}, img= img)
	_addon.end_of_directory()

def listSeasons(section, url, img=''): #_param['img']
	xbmcplugin.setContent( int( sys.argv[1] ), 'seasons' )
	WhereAmI('@ the Seasons List for TV Show -- url: %s' % url)
	html = net.http_GET(url).content
	if (html=='') or (html=='none') or (html==None):
		if (_debugging==True): print 'Html is empty.'
		return
	if (img==''):
		match=re.search( 'coverImage">.+?src="(.+?)"', html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
		img=match.group(1)
	#seasons=re.compile('onclick="return toggleSeason('(\d+)');">', re.IGNORECASE | re.DOTALL).findall(html)
	#seasons=re.compile('onclick="return toggleSeason(\'(\d+)\');">').findall(html)
	#if (_debugging==True): print ParseDescription(html)
	seasons=re.compile("toggleSeason\('(\d+)'\)").findall(html)
	if (_debugging==True): print seasons
	if not seasons: 
		if (_debugging==True): print 'couldn\'t find seasons'
		return
	for season_name in seasons:
		season_name = season_name.replace( '_',  ' ')
		addon.add_directory({'mode': 'GetEpisodes', 'year': _param['year'], 'section': section, 'img': img, 'url': url, 'season': season_name}, {'title':  'Season '+season_name}, img= img)
	_addon.end_of_directory()
	##
	#shows = re.compile('<a class="behavior_trigger_season.+?id="trigger_(.+?)"(.+?)<h4>', re.DOTALL).findall(html)   
	#if not shows: 
	#	if (_debugging==True): print 'couldn\'t find seasons'
	#else:
	#	for season_name, episodes in shows:
	#		season_name = season_name.replace( '_',  ' ')
	#		addon.add_directory({'mode': 'GetEpisodes', 'section': section, 'img': img, 'episodes': episodes.encode('utf-8')}, {'title':  season_name}, img= img)
	#	_addon.end_of_directory()




#_param['genre']
#int(datetime.date.today().strftime("%Y"))
          
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
def check_mode(mode=''):
	deb('Mode',mode)
	if (mode=='') or (mode=='main') or (mode=='MainMenu'): 
		initDatabase()
		Menu_MainMenu()
	elif (mode=='ResolverSettings'): urlresolver.display_settings()
	elif (mode=='Settings'): _plugin.openSettings()
	elif (mode=='PlayVideo'): PlayVideo(_param['url'], _param['infoLabels'], _param['listitem'])
	elif (mode=='LoadCategories'): Menu_LoadCategories(_param['section'])
	#elif (mode=='BrowseAtoZ'): BrowseAtoZ(_param['section'])
	elif (mode=='BrowseYear'): Menu_BrowseByYear(_param['section'])
	elif (mode=='BrowseGenre'): Menu_BrowseByGenre(_param['section'])
	#elif (mode=='BrowseLatest'): BrowseLatest(_param['section'])
	#elif (mode=='BrowsePopular'): BrowsePopular(_param['section'])
	#elif (mode=='GetResults'): GetResults(_param['section'], genre, letter, page)
	elif (mode=='GetTitles'): listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'])
	elif (mode=='GetTitlesLatest'): listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck='Latest')
	elif (mode=='GetTitlesPopular'): listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck='Popular')
	elif (mode=='GetTitlesHDPopular'): listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck='HDPopular')
	elif (mode=='GetTitlesOtherPopular'): listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck='OtherPopular')
	elif (mode=='GetTitlesNewPopular'): listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck='NewPopular')
	elif (mode=='GetLinks'): listLinks(_param['section'], _param['url'], showtitle=_param['showtitle'], showyear=_param['showyear'])
	elif (mode=='GetSeasons'): listSeasons(_param['section'], _param['url'], _param['img'])
	elif (mode=='GetEpisodes'): listEpisodes(_param['section'], _param['url'], _param['img'], _param['season'])
	elif (mode=='TextBoxFile'): TextBox2().load_file(_param['url'],_param['title'])
	elif (mode=='TextBoxUrl'):  TextBox2().load_url( _param['url'],_param['title'])
	elif (mode=='SearchForAirDates'):  search_for_airdates(_param['title'])
	#elif (mode=='GetSearchQuery'): GetSearchQuery(_param['section'])
	#elif (mode=='Search'): Search(_param['section'], query)

### ############################################################################################################
deb('param >> url',_param['url'])
check_mode(_param['mode'])

### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
