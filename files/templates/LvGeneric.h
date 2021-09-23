/*
 * Lv/*WNAME*/.h
 *
 */

#ifndef LV/*WCAP*/_H_
#define LV/*WCAP*/_H_

#include "../core/lvglpp.h"
/*WINCLUDE*/

namespace lvglpp {

class Lv/*WNAME*/ {
private:
	/*WPRIVATE*/
	LvPointer<lv_/*WTYPE*/_t, /*WDELETE*/> cObj;
public:
	Lv/*WNAME*/();
	virtual ~Lv/*WNAME*/();
	lv_/*WTYPE*/_t* raw();/*METHODS*/
};

} /* namespace lvglpp */

#endif /* LV/*WCAP*/_H_ */
