/*
 * $classname.h
 *
 */

#ifndef $uppername
#define $uppername

#include "../core/lvglpp.h"

namespace lvglpp {

class $classname {
private:
	$private
	LvPointer $objdef  cObj;
public:
	$classname () {cObj.reset($alloc(sizeof($name)));}
	operator $name*() const {
		return cObj.get();
	}
	$methods
};

} /* namespace lvglpp */

#endif /* $uppername */
