from tqdm import tqdm

lbar = None

def print_progress_state(_cur,_tot,_nam):	
	global lbar
	if lbar is not None and ((type(_nam) is not str and lbar.desc != _nam.decode('utf-8')) or (type(_nam) is str and lbar.desc != _nam)):
		lbar.close()
		lbar = None
		
	if lbar is None:
		if type(_nam) is not str:
			lbar = tqdm(total=_tot, desc=_nam.decode('utf-8'))
		else:
			lbar = tqdm(total=_tot, desc=_nam)
	lbar.update(_cur - lbar.n)
	
	if _cur == _tot:
		lbar.close()
		lbar = None

def opt_progress_state(state_p):
	state = state_p.contents
	global lbar
	
	if lbar is None:
		lbar = tqdm(total=state.max_iterations)

	lbar.set_description( "{:.4f};{:.4f}".format(state.best_norm,state.best_obj) )
	lbar.update(1)
	
	if state.iteration == state.max_iterations:
		lbar.close()
		lbar = None
