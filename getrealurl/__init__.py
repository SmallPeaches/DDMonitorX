
def get_stream_url(platform,rid,type='flv'):
    stream_url = None
    
    if platform in ['hy','huya']:
        from . import huya
        url = huya.get_real_url(rid)
        if url.startswith('http'):
            stream_url = url
        elif ('未开播' in url) or ('直播录像' in url):
            raise RuntimeError('未开播')
        else:
            raise RuntimeError('无法解析URL')
    
    elif platform in ['bili','bilibili']:
        from . import bilibili
        if type == 'm3u8':
            url_dict = bilibili.get_real_url(rid)['m3u8']
            key = list(url_dict)[0]
            stream_url = url_dict[key]
        else: 
            stream_url = bilibili.get_real_url(rid)['flv']

    elif platform in ['dy','douyu']:
        from . import douyu
        url = douyu.get_real_url(rid)
        stream_url = url
    
    if not stream_url:
        raise ValueError('无法解析URL')
    
    return stream_url
        