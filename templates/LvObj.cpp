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


} /* namespace lvglpp */
