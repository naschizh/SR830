import pyvisa
from time import sleep

def list_ports():
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())

class LockInSR830:

    FMOD = ['External', 'Internal']
    RSLP = ['Sine zero crossing', 'TTL rising edge', 'TTL falling edge']
    SENS = [2e-9, 5e-9, 10e-9, 20e-9, 50e-9, 100e-9, 200e-9,
            500e-9, 1e-6, 2e-6, 5e-6, 10e-6, 20e-6, 50e-6, 100e-6,
            200e-6, 500e-6, 1e-3, 2e-3, 5e-3, 10e-3, 20e-3,
            50e-3, 100e-3, 200e-3, 500e-3, 1]
    RMOD = ['High Reserve', 'Normal', 'Low Noise']
    OFLT = [10e-6, 30e-6, 100e-6, 300e-6, 1e-3, 3e-3, 10e-3,
            30e-3, 100e-3, 300e-3, 1, 3, 10, 30, 100, 300, 1e3,
            3e3, 10e3, 30e3]
    OFSL = ['6 dB/oct', '12 dB/oct', '18 dB/oct', '24 dB/oct']
    SYNC = ['Off', 'On']
    ISRC = ['A', 'A-B', 'I (1MOhm)', 'I (100MOhm)']
    IGND = ['Float', 'Ground']
    ICPL = ['AC', 'DC']
    ILIN = ['Out or no filters', 'Line notch in', '2xLine notch in', 'Both notch filters in']
    DDEF = {'CH1': {'j': ['X', 'R', 'X Noise', 'Aux In 1', 'Aux In 2'], 'k': ['none', 'Aux In 1', 'Aux In 2']},
            'CH2': {'j': ['Y', 'Theta', 'Y Noise', 'Aux In 3', 'Aux In 4'], 'k': ['none', 'Aux In 3', 'Aux In 4']}}
    OEXP_expand = [1, 10, 100]
    AOFF = ['X', 'Y', 'R']

    def __init__(self, port=None):
        self.port = port
        self.rm = pyvisa.ResourceManager()

    def query_visa(self, command):
        li = self.rm.open_resource(self.port, write_termination = '\n', read_termination='\n')
        response = li.query(command)
        li.clear()
        li.close()
        return response

    def write_visa(self, command):
        li = self.rm.open_resource(self.port, read_termination='\n',  write_termination = '\n')
        li.write(command)
        li.clear()
        li.close()

    """REFERENCE AND PHASE METHODS"""

    #getting and setting the harmonic value
    @property
    def harm(self):
        print('Getting the HARM value.')
        harm = self.query_visa('HARM?')
        return harm

    @harm.setter
    def harm(self, value):
        print(f'Setting the HARM value for value = {value}.')
        self.write_visa(f'HARM {value}')

    #getting and setting the reference source
    @property
    def fmod(self):
        print('Getting the FMOD value.')
        fmod = self.query_visa('FMOD?')
        return self.FMOD[int(fmod)]

    @fmod.setter
    def fmod(self, value):
        print(f'Setting the FMOD value for value = {value}.')
        self.write_visa(f'FMOD {self.FMOD.index(value)}')

    #getting and setting the reference phase shift
    @property
    def phas(self):
        print('Getting the PHAS value.')
        phas = float(self.query_visa('PHAS?'))
        return phas

    @phas.setter
    def phas(self, value):
        phas_value = value - 360.0 - 360.0
        print(f'Setting the PHAS value for value = {value} ({phas_value}).')
        self.write_visa(f'PHAS {value}')

    #getting and setting the reference frequency
    @property
    def freq(self):
        print('Getting the FREQ value.')
        freq = float(self.query_visa('FREQ?'))
        return freq

    @freq.setter
    def freq(self, value):
        print(f'Setting the FREQ value for value = {value}.')
        self.write_visa(f'FREQ {value}')

    #getting and setting the reference trigger when using the external reference mode
    @property
    def rslp(self):
        print('Getting the RSLP value.')
        rslp = self.query_visa('RSLP?')
        return self.RSLP[int(rslp)]

    @rslp.setter
    def rslp(self, value):
        print(f'Setting the RSLP value for value = {value}.')
        self.write_visa(f'RSLP {self.RSLP.index(value)}')

    #getting and setting the amplitude of the sine output
    @property
    def slvl(self):
        print('Getting the SLVL value.')
        slvl = float(self.query_visa('SLVL?'))
        return slvl

    @slvl.setter
    def slvl(self, value):
        print(f'Setting the SLVL value for value = {value}.')
        self.write_visa(f'SLVL {value}')

    """GAIN AND TIME CONSTANT COMMANDS"""

    #shows the table of available sensitivities
    def show_sens(self):
        print('\nThe sensitivity table')
        print('{:<8} {:<15}'.format('Index', 'Sensitivity'))
        for i in range(0, len(self.SENS)):
            print('{:<8} {:<15}'.format(i, self.SENS[i]))
        print('\n')

    #getting and setting the sensitivity
    @property
    def sens(self):
        print('Getting the SENS value.')
        sens = self.query_visa('SENS?')
        sens = int(sens)
        return self.SENS[sens]

    @sens.setter
    def sens(self, value):
        print(f'Setting the SENS value for value = {value}.')
        self.write_visa(f'SENS {self.SENS.index(value)}')

    def sens_next(self):
        sens = self.query_visa('SENS?')
        index = int(sens) + 1
        if index < len(self.SENS):
            self.write_visa(f'SENS {index}')
        else:
            pass

    def sens_previous(self):
        sens = self.query_visa('SENS?')
        index = int(sens) - 1
        if index >= 0:
            self.write_visa(f'SENS {index}')
        else:
            pass

    #shows the table of available reserve modes
    def show_rmod(self):
        print('\nThe reserve mode table')
        print('{:<8} {:<15}'.format('Index', 'Reserve mode'))
        for i in range (0, len(self.RMOD)):
            print('{:<8} {:<15}'.format(i, self.RMOD[i]))
        print('\n')

    #setting and getting the reserve mode
    @property
    def rmod(self):
        print('Getting the RMOD value.')
        rmod = self.query_visa('RMOD?')
        rmod = int(rmod)
        return self.RMOD[rmod]

    @rmod.setter
    def rmod(self, value):
        print(f'Setting the RMOD value for value = {value}.')
        self.write_visa(f'RMOD {self.RMOD.index(value)}')

    #shows the table of available time constants
    def show_oflt(self):
        print('\nThe time constant table')
        print('{:<8} {:<15}'.format('Index', 'Time constant'))
        for i in range (0, len(self.OFLT)):
            print('{:<8} {:<15}'.format(i, self.OFLT[i]))
        print('\n')

    #setting and getting the time constant
    @property
    def oflt(self):
        print('Getting the OFLT value.')
        command = 'OFLT?'
        oflt = self.query_visa(command)
        return self.OFLT[int(oflt)]

    @oflt.setter
    def oflt(self, value):
        assert value <= 30e3, 'Time constant must be smaller than 30ks.'
        if value not in self.OFLT:
            for tc in self.OFLT:
                if tc > value:
                    value = tc
                    break
        print(f'Setting the OFLT value for value = {value}.')
        self.write_visa(f'OFLT {self.OFLT.index(value)}')

    #shows the table of available low pass filter slopes
    def show_ofsl(self):
        print('\nThe low pass filter slopes table')
        print('{:<8} {:<15}'.format('Index', 'Low pass filter slope'))
        for i in range (0, len(self.OFSL)):
            print('{:<8} {:<15}'.format(i, self.OFSL[i]))
        print('\n')

    #setting and getting the low pass filter slope
    @property
    def ofsl(self):
        print('Getting the OFSL value.')
        ofsl = self.query_visa('OFSL?')
        ofsl = int(ofsl)
        return self.OFSL[ofsl]

    @ofsl.setter
    def ofsl(self, value):
        print(f'Setting the OFSL value for value = {value}.')
        self.write_visa(f'OFSL {self.OFSL.index(value)}')

    #setting and getting the synchronous filter status
    @property
    def sync(self):
        print('Getting the SYNC value.')
        sync = self.query_visa('SYNC?')
        sync = int(sync)
        return self.SYNC[sync]

    @sync.setter
    def sync(self, value):
        print(f'Setting the SYNC value for value = {value}.')
        self.write_visa(f'SYNC {self.SYNC.index(value)}')

    """INPUT AND FILTER COMANDS"""

    #shows the table of input configurations
    def show_isrc(self):
        print('\nThe input configuration table')
        print('{:<8} {:<15}'.format('Index', 'Input configuration'))
        for i in range (0, len(self.ISRC)):
            print('{:<8} {:<15}'.format(i, self.ISRC[i]))
        print('\n')

    #setting and getting the input configuration
    @property
    def isrc(self):
        print('Getting the ISRC value.')
        isrc = self.query_visa('ISRC?')
        isrc = int(isrc)
        return self.ISRC[isrc]

    @isrc.setter
    def isrc(self, value):
        print(f'Setting the ISRC value for value = {value}.')
        self.write_visa(f'ISRC {self.ISRC.index(value)}')

    #setting and getting the input sheild grounding
    @property
    def ignd(self):
        print('Getting the IGND value.')
        ignd = self.query_visa('IGND?')
        ignd = int(ignd)
        return self.IGND[ignd]

    @ignd.setter
    def ignd(self, value):
        print(f'Setting the IGND value for value = {value}.')
        self.write_visa(f'IGND {self.IGND.index(value)}')

    #setting and getting the input coupling
    @property
    def icpl(self):
        print('Getting the ICPL value.')
        icpl = self.query_visa('ICPL?')
        icpl = int(icpl)
        return self.ICPL[icpl]

    @icpl.setter
    def icpl(self, value):
        #print(f'Setting the ICPL value for value = {value}.')
        self.write_visa(f'ICPL {self.ICPL.index(value)}')

    #shows the table of input line notch filter statuses
    def show_ilin(self):
        print('\nThe input line notch filter statuses table')
        print('{:<8} {:<15}'.format('Index', 'Input line notch filter status'))
        for i in range (0, len(self.ILIN)):
            print('{:<8} {:<15}'.format(i, self.ILIN[i]))
        print('\n')

    #setting and getting the input line notch filter status
    @property
    def ilin(self):
        print('Getting the ILIN value.')
        ilin = self.query_visa('ILIN?')
        ilin = int(ilin)
        return self.ILIN[ilin]

    @ilin.setter
    def ilin(self, value):
        print(f'Setting the ILIN value for value = {value}.')
        self.write_visa(f'ILIN {self.ILIN.index(value)}')

    """DISPLAY AND OUTPUT COMMANDS"""

    #shows the table of CH1 and CH2 displays
    def show_ddef(self):
        print('\nThe CH1 and CH2 displays')
        print('{:<20} {:<40}'.format('CH1 (i = 1)', 'CH2 (i = 2)'))
        print('{:<8} {:<16} {:<8} {:<16}'.format('j', 'display', 'j', 'display'))
        for j in range(0, len(self.DDEF['CH1']['j'])):
            print('{:<8} {:<16} {:<8} {:<16}'.format(j, self.DDEF['CH1']['j'][j], j, self.DDEF['CH2']['j'][j]))
        print('{:<8} {:<16} {:<8} {:<16}'.format('k', 'ratio', 'k', 'ratio'))
        for k in range(0, len(self.DDEF['CH1']['k'])):
            print('{:<8} {:<16} {:<8} {:<16}'.format(k, self.DDEF['CH1']['k'][k], k, self.DDEF['CH2']['k'][k]))
        print('\n')

    #setting and getting the display and ratio of the display
    @property
    def ddef(self):
        print('Getting the DDEF value.')
        ch1 = list(self.query_visa(f'DDEF? 1'))
        ch2 = list(self.query_visa(f'DDEF? 2'))
        ddef = {'CH1': [self.DDEF['CH1']['j'][int(ch1[0])], self.DDEF['CH1']['k'][int(ch1[2])]],
                'CH2': [self.DDEF['CH2']['j'][int(ch2[0])], self.DDEF['CH2']['k'][int(ch2[2])]]}
        return ddef

    @ddef.setter
    def ddef(self, values):
        print('Setting the DDEF values.')
        value_i, value_j, value_k = values
        if value_i == 'CH1':
            i = 1
        elif value_i == 'CH2':
            i = 2
        j = self.DDEF[value_i]['j'].index(value_j)
        k = self.DDEF[value_i]['k'].index(value_k)
        self.write_visa(f'DDEF {i} {j} {k}')

    """AUX INPUT AND OUTPUT COMMANDS"""

    """SETUP COMMANDS"""

    """AUTO FUNCTIONS"""

    """DATA STORAGE COMMANDS"""

    """DATA TRANSFER COMMANDS"""

    #shows the table of commands
    def show_outp(self):
        print('\nThe otput table')
        print('{:<8} {:<15}'.format('Index', 'Commands'))
        for i in range (1, len(self.OUTP)):
            print('{:<8} {:<15}'.format(i, self.OUTP[i]))
        print('\n')

    #getter of x
    @property
    def outp_x(self):
        #print('Getting the OUTP X value.')
        outp_x = self.query_visa('OUTP? 1')
        return float(outp_x)

    #getter of y
    @property
    def outp_y(self):
        #print('Getting the OUTP Y value.')
        outp_y = self.query_visa('OUTP? 2')
        return float(outp_y)

    #getter of r
    @property
    def outp_r(self):
        #print('Getting the OUTP R value.')
        outp_r = self.query_visa('OUTP? 3')
        return float(outp_r)

    #getter of theta
    @property
    def outp_theta(self):
        #print('Getting the OUTP THETA value.')
        outp_theta = self.query_visa('OUTP? 4')
        return float(outp_theta)
