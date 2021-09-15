/*
 * LvObj.h
 *
 *  Created on:
 *      Author: fstuffdev
 */

#ifndef LVOBJ_H_
#define LVOBJ_H_

#include "lvglpp.h"

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

};

} /* namespace lvglpp */

#endif /* LVOBJ_H_ */
