/*
 * Lv/*WNAME*/.cpp
 *
 */

#include "Lv/*WNAME*/.h"

namespace lvglpp {

Lv/*WNAME*/::Lv/*WNAME*/() {
	cObj.reset(/*WALLOC*/);
	/*WPOSTINIT*/
}

Lv/*WNAME*/::~Lv/*WNAME*/() {
}

lv_/*WTYPE*/_t* Lv/*WNAME*/::raw() {
	return cObj.get();
}/*METHODS*/

} /* namespace lvglpp */
