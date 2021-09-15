/*
 * LvObj.cpp
 *
 *  Created on: Jun 24, 2021
 *      Author: fstuffdev
 */

#include "LvObj.h"

namespace lvglpp {

LvObj::LvObj() : LvObj(NULL){

}
LvObj::LvObj(LvObj* Parent) {
	if(Parent)
		cObj.reset(lv_obj_create(Parent->raw()));
	else
		cObj.reset(lv_obj_create(lv_scr_act()));
}
lv_obj_t* LvObj::raw() {
	return cObj.get();
}
LvObj::~LvObj() {

}
LvObj& LvObj::setCObj(lv_obj_t* _cObj) {
	if(_cObj)
		cObj.reset(_cObj);
	return *this;
}/*METHODS*/

/* The Cpp event dispatcher */
void LvObj::EventDispatcher(lv_event_t *e) {

	LvObj *_Obj = static_cast<LvObj*>(e->user_data);

	std::list<eventBind_t>::iterator eventIter;

	if (_Obj) {
		/* Search in registered events */
		for (eventIter = _Obj->eventRegister.begin();
				eventIter != _Obj->eventRegister.end(); eventIter++) {
			if (eventIter->evCode == e->code) {
				/* Call the event */
				if (eventIter->evCallback)
					(*(eventIter->evCallback))(e);
			}
		}
	}
}

/* Enable the related code Callback */
LvObj& LvObj::setCallback(lv_event_code_t code, LvEvent *Cb) {

	eventBind_t eventToRegister;
	eventToRegister.evCallback = Cb;
	eventToRegister.evCode = code;

	/* Setting Callback to EventDispatcher sacrificing user_data of callback */
	this->addEventCb(LvObj::EventDispatcher, code, (void*) this);

	eventRegister.push_back(eventToRegister);

	return *this;
}

} /* namespace lvglpp */
