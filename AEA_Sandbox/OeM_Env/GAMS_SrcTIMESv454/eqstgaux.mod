*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
* Copyright (C) 2000-2021 Energy Technology Systems Analysis Programme (ETSAP)
* This file is part of the IEA-ETSAP TIMES model generator, licensed
* under the GNU General Public License v3.0 (see file LICENSE.txt).
*=============================================================================*
* EQSTGAUX auxiliary commodities for storage
*=============================================================================*
*AL Questions/Comments:
* Assumption is that all auxiliary flows are at PRC_TS level; NST primary flows can be also above
*-----------------------------------------------------------------------------*
*$ONLISTING


  %EQ%_STGAUX(RTP_VINTYR(%R_V_T%,P),C,RTS(S)%SWT%)$((RPCS_VAR(R,P,C,S)*(NOT RPC_STG(R,P,C)+RPC_EMIS(R,P,C)))$RP_STG(R,P))..

* Auxiliary flow variable
    %VAR%_FLO(R,V,T,P,C,S %SOW%)

    =E=

* flow depends on storage level in period T
    SUM(ANNUAL(SL),PRC_ACTFLO(R,V,P,C) *
        (
         SUM(PRC_TS(R,P,TS)$TS_MAP(R,TS,S),%VAR%_ACT(R,V,T,P,TS %SOW%)/RS_STGPRD(R,TS)) * G_YRFR(R,S) -
* subtract in- and output flows to/from storage during latter half of period (from middle of M(T))
         SUM(TOP(PRC_STGIPS(R,P,COM),IO),
           (%VAR%_SIN(R,V,T,P,COM,SL%SOW%)$IPS(IO) - %VAR%_SOUT(R,V,T,P,COM,SL%SOW%)$(NOT IPS(IO)))/PRC_ACTFLO(R,V,P,COM)) *
         SUM(PERIODYR(T,Y_EOH)$(YEARVAL(Y_EOH) GE M(T)), 
* storage losses (assume that Inflows and outflows occur at the mid-point of each year)
           MIN(1,YEARVAL(Y_EOH)-M(T)+MAX(0,M(T)+D(T)/2-E(T))) * ((1-STG_LOSS(R,V,P,SL))**(E(T)-YEARVAL(Y_EOH)+0.5)))
* For IPS, MID storage level is (1-LOSS)**(E(T)-M(T)+0.5) higher
        ) * (1+((1-STG_LOSS(R,V,P,SL))**(M(T)-E(T)-MIN(0.5,MAX(0,M(T)+D(T)/2-E(T))))-1)$PRC_MAP(R,'STK',P))) +

* flow depends on storage in- or outflow in period T
    SUM((COM_GMAP(R,CG,COM),TOP(RPC_STG(R,P,COM),'IN'),RPCS_VAR(R,P,COM,TS))$COEF_PTRAN(R,V,P,CG,COM,C,TS),
        (%VAR%_SIN(R,V,T,P,COM,TS %SOW%) * COEF_PTRAN(R,V,P,CG,COM,C,TS))$((NOT PRC_MAP(R,'NST',P))+PRC_NSTTS(R,P,TS)) *
         RS_FR(R,S,TS) * (1+RTCS_FR(R,T,C,S,TS))) +
    SUM((COM_GMAP(R,CG,C),TOP(RPC_STG(R,P,COM),'OUT'),RPCS_VAR(R,P,COM,TS))$COEF_PTRAN(R,V,P,CG,C,COM,S),
        (%VAR%_SOUT(R,V,T,P,COM,TS %SOW%) * (1/COEF_PTRAN(R,V,P,CG,C,COM,S)))$(PRC_NSTTS(R,P,TS) EQV RPC_STGN(R,P,COM,'OUT')) *
         RS_FR(R,S,TS) * (1+RTCS_FR(R,T,C,S,TS)))

;

$OFFLISTING
