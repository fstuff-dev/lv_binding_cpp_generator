/*
 * LvDisp.h
 *
 */

#ifndef LVDISP_H_
#define LVDISP_H_

#include "LvObj.h"

namespace lvglpp {

class LvDisp: public LvObj {
public:
	LvDisp();
	LvDisp(LvObj* Parent);
	virtual ~LvDisp() override;/*METHODS*/
};

} /* namespace lvglpp */

#endif /* LVDISP_H_ */
