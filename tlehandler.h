#ifndef _TLE_HANDLER_H_
#define _TLE_HANDLER_H_

struct view_angles
{
	float azimuth;
	float elevation;
};
typedef struct view_angles VIEW_ANGLES;

void TLE_Handler_Init(void);
void TLE_Handler_SetNewTLE(char * l0, char * l1, char * l2);
void TLE_Handler_Update(TM * time);

void TLE_Handler_GetViewAngles(VECTOR_3D * observer, VIEW_ANGLES * viewAngles);

#endif
