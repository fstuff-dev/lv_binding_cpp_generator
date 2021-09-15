/*
 * LvObj.h
 *
 *  Created on:
 *      Author: fstuffdev
 */

#ifndef LVOBJ_H_
#define LVOBJ_H_

#include <list>
#include "lvglpp.h"
#include "LvEvent.h"


namespace lvglpp {

class LvObj {
protected:
	LvPointer<lv_obj_t, lv_obj_del> cObj;
public:

	/* Creation and deletion */
	LvObj();
	LvObj(LvObj *Parent);
	virtual ~LvObj();
	lv_obj_t* raw();
	LvObj& setCObj(lv_obj_t* _cObj);/*METHODS*/

	/* Cpp Event Management*/
	typedef struct {
		lv_event_code_t evCode;
		LvEvent* evCallback;
	}eventBind_t;

	/* List of registered events */
	std::list<eventBind_t> eventRegister;
	static void EventDispatcher(lv_event_t* e);
	LvObj& setCallback(lv_event_code_t code,LvEvent* Cb);

};

} /* namespace lvglpp */

#endif /* LVOBJ_H_ */
