import asyncio, random, copy


########## config ############
halt_chance_range = 4  # Testers will halt if random.randrange(0, halt_chance_range) returns a 0
total_tester_number = 6
max_concurrent_testers = 3
########## config ############


########## global variables ############
running_tester_count = 0
history_tester_count = 0
########## global variables ############


async def random_halt(tester_index, used_time):
	""" use recursive structure to demonstrate how to call another async function """

	random_factor = random.randrange(0, halt_chance_range)
	if random_factor == 0 and used_time != 0 :
		print(f'tester.{tester_index} has stopped after {used_time} seconds.')
		return used_time

	print(f'tester.{tester_index} waiting .... {used_time}')
	await asyncio.sleep(1)
	return await random_halt(tester_index, used_time + 1)

async def run_a_new_test(tester_index):
	"""
	 Wrap this async function in a new thread,
 	 so that the main function won't have to 'await' it.
	"""
	global running_tester_count

	await random_halt( tester_index, 0 )
	running_tester_count -= 1

async def main():
	global running_tester_count
	global history_tester_count

	tasks = set()

	while history_tester_count < total_tester_number:
		# Create new tester only when there is still space, 
		if running_tester_count < max_concurrent_testers:
			running_tester_count += 1
			history_tester_count += 1
			print(f'\n        starting tester : {history_tester_count}   \n')
			task = asyncio.create_task(run_a_new_test(history_tester_count))
			task.add_done_callback(lambda t: [
									 	#print(f'  task is done : {t}'),
										tasks.discard(t)
									 ])
			tasks.add(task)
		else: # otherwise check again later
			await asyncio.sleep(1)

	# Wait until all tasks are finished
	while tasks:
		await asyncio.sleep(1)


# async def main_with_thread(): 
# 	import threading
# 	global running_tester_count
# 	global history_tester_count

# 	while history_tester_count < total_tester_number:
# 		# Create new tester only when there is still space, otherwise check again later
# 		if running_tester_count < max_concurrent_testers:
# 			running_tester_count += 1
# 			history_tester_count += 1
# 			_thread = threading.Thread(target=asyncio.run, args=(run_a_new_test(history_tester_count), ))
# 			print(f'        starting tester : {history_tester_count}   ')
# 			_thread.start()
# 		else:
# 			await asyncio.sleep(1)

# 	# Wait until all threads are finished
# 	while running_tester_count > 0:
# 			await asyncio.sleep(1)


if __name__ == '__main__':
	asyncio.run(main())
	print("\nAll Done.")