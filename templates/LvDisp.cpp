/*
 * LvDisp.cpp
 *
 */

#include "LvDisp.h"

namespace lvglpp {

LvDisp::LvDisp() : LvDisp(NULL) {
}

LvDisp::LvDisp(LvObj* Parent) : LvObj(Parent) {
	setUserData(this);
}

LvDisp::~LvDisp() {
}/*METHODS*/

} /* namespace lvglpp */
