
# General Info  
##### VAR_FLOW

    ['R', 'ALLYEAR', 'ALLYEAR', 'P', 'C', 'S']

    R ~         Region
    ALLYEAR ~   All Years # Todo find out diff between ALLYEAR and ALLYEAR  
    ALLYEAR ~   All Years # Todo find out
    P ~         Processes
    C ~         Commodities
    S ~         The universe for time-slices


# General Data MGNT 
* where do i find suitable translations?
* how do we organize the the pseudo hierarchical structure of the energy carrier which is required by pyam 
* do all models have the same structure?
    * I have noiced that `BasiModel.gdx` dose not have the same structure as `OEM-Jan-Base.gdx`
    * At least `gdx_db["VAR_FLO"].get_dimensions_as_string()` returns differnet out put
    * expected to be `['R', 'ALLYEAR', 'ALLYEAR', 'P', 'C', 'S']`

#   EASY Questions
* whats up with `ALLYEAR` in VAR_FLO?
* what are the `UNITS` we should use in pyam dataformat?
    
    
    >> This is a code box 
    >> x = "use"
    >> y = "me"
    >> print(x + " " + y + "!")

    
# TASKS
# NOTES
process = "EGRDELC00"
commoditty = "ELCELC"

# Variables of interest
VAR_FLO
VAR_CAP 
VAR_NCAP
VAR_CUMPROD
VAR_ACT

# parameter 
# todo 
