### ############################################################################################################
###	#	
### # Project: 			#		Config.py - by The Highway 2013.
### # Author: 			#		The Highway
### # Version:			#		(ever changing)
### # Description: 	#		My Project Config File
###	#	
### ############################################################################################################
### ############################################################################################################
### Imports ###
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
import re,os,sys,string,StringIO,logging,random,array,time,datetime
from t0mm0.common.addon import Addon

### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
### Plugin Settings ###
def ps(x):
	return {
		'__plugin__': 					"[COLOR goldenrod]S[/COLOR]olarmovie.so"
		,'__authors__': 				"[COLOR white]The[COLOR tan]Highway[/COLOR][/COLOR]"
		,'__credits__': 				"anilkuj of plugin.video.soloremovie (solarmovie.eu) for much initial work, TheHighway of plugin.video.theanimehighway for teh_tools.py"
		,'_addon_id': 					"plugin.video.solarmovie.so"
		,'_plugin_id': 					"plugin.video.solarmovie.so"
		,'_domain_url': 				"http://www.solarmovie.so"
		,'_database_name': 			"solarmovieso"
		,'_addon_path_art': 		"art"
		,'GENRES': 							['Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western']
		,'default_art_ext': 		'.png'
		,'default_cFL_color': 	'goldenrod'
		,'default_section': 		'movies'
		,'meta.movie.domain': 	'http://www.themoviedb.org'
		,'meta.movie.search': 	'http://www.themoviedb.org/search?query=TT'
		,'meta.tv.domain': 			'http://www.thetvdb.com'
		,'meta.tv.search': 			'http://www.thetvdb.com/index.php?seriesname=&fieldlocation=2&language=7&genre=&year=&network=&zap2it_id=&tvcom_id=&order=translation&addedBy=&searching=Search&tab=advancedsearch&imdb_id=TT'
		,'meta.tv.page': 				'http://www.thetvdb.com/index.php?tab=series&lid=7&id='
		,'meta.tv.fanart.url': 	'http://www.thetvdb.com/banners/fanart/original/'
		,'meta.tv.fanart.url2': '-1.jpg'
#		,'': 
#		,'': 
	}[x]
_art_DefaultExt  ='.png'
_cFL_DefaultColor='goldenrod'

### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
### For Multiple Methods ###

### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
### Other Settings ###
GENRES = ['Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western']


### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
### Configurable Functions ###

### ############################################################################################################
