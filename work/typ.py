
matchingTable = (
    
    #lv_obj
    ("lv_obj_t","LvObj"),
    ("lv_obj_t*","LvObj"),
    ("lv_obj_t *","LvObj"),
    
    #lv_style
    ("lv_style_t","LvStyle"),
    ("lv_style_t*","LvStyle"),
    ("lv_style_t *","LvStyle"),
    
    #lv_anim
    ("lv_anim_t","LvAnim"),
    ("lv_anim_t*","LvAnim"),
    ("lv_anim_t *","LvAnim"),
    
    #lv_anim_timeline
    ("lv_anim_timeline_t","LvAnimTimeline"),
    ("lv_anim_timeline_t*","LvAnimTimeline"),
    ("lv_anim_timeline_t *","LvAnimTimeline")
    
    )

def typeMatch(itype):
    for typ in matchingTable:
        if(itype == typ[0]):
            return typ[1]
    return None