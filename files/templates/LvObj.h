/*
 * LvObj.h
 *
 *  Created on:
 *      Author: fstuffdev
 */

#ifndef LVOBJ_H_
#define LVOBJ_H_

#include "lvglpp.h"
#include <type_traits>

namespace lvglpp {

template <typename derivedClass>
class LvBaseObj {
protected:
	LvPointer<lv_obj_t, lv_obj_del> cObj;
public:

	using derivedType = std::remove_cv_t<derivedClass>;

	LvBaseObj(lv_obj_t* parent = nullptr) : cObj(parent ? parent : lv_scr_act())  {

		lv_obj_set_user_data(cObj.get(), this);

	}

	operator lv_obj_t*() const {

		return cObj.get();

	}

	operator derivedType&() {

		return reinterpret_cast<derivedType&>(*this);

	}$methods

};

class LvObj : public LvBaseObj<LvObj> {
public:
	LvObj(lv_obj_t* parent = nullptr) : LvBaseObj(lv_obj_create(parent ? parent : lv_scr_act())) {};
};

} /* namespace lvglpp */

#endif /* LVOBJ_H_ */
