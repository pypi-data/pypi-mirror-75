from pyvmodule.develope import VModule,VStruct,Wire,Reg,Always
class ClockEnable(VStruct):
    def __init__(self,**kwargs):
        VStruct.__init__(self,**kwargs)
    @property
    def module(self):
        class clock_gating_unit(VModule):
            clock = Wire(io='input')
            next  = Wire(io='input')
            mask  = Reg (clock_enable=True)
            subclock = Wire(io='output')
            Always(clock)[mask:~next]
            subclock[:] = clock|mask
        return clock_gating_unit
