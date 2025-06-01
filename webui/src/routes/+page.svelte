<script lang="ts">
	let eel = window.eel;
	let input_value = '';
	eel?.set_host('ws://localhost:8888');
	import { Application } from '@splinetool/runtime';
	import { onMount } from 'svelte';
	onMount(() => {
		// @ts-expect-error html element
		const canvas: HTMLCanvasElement = document.getElementById('canvas3d');
		const app = new Application(canvas);
		app.load('https://prod.spline.design/NNfGHj4gsBiVtyuU/scene.splinecode');
	});
</script>

<div class="absolute left-0 right-0 text-center opacity-90">
	<div class="relative">
		<canvas id="canvas3d" />
		<div class="flex justify-between ">
			<div>
				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={() => eel?.mute_system()()}
				>
					Mute
				</button>
				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={() => eel?.unmute_system()()}
				>
					Unmute
				</button>
				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={() => eel?.set_volume_up()()}
				>
					Volume Up
				</button>
				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={() => eel?.set_volume_down()()}
				>
					Volume Down
				</button>
			</div>
			<div>
				<input
					placeholder="Enter command"
					class="bg-black border-white border rounded-md m-4 p-2 text-black"
					bind:value={input_value}
					on:keydown={(e) => {
						if (e.key === 'Enter') {
							// @ts-expect-error html element
							eel?.send_command(e.target.value)();
							// @ts-expect-error html element
							e.target.value = '';
						}
					}}
				/>
			</div>
			<div class="grid grid-cols-3">
				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={() => {
						eel?.llm_chat(input_value)();
						input_value = '';
					}}
				>
					Ask llm
				</button>
				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={() => {
						eel?.realtime_chat(input_value)();
					}}
				>
					Ask Real time llm
				</button>
				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={() => {
						eel?.open_app(input_value)();
					}}
				>
					Open
				</button>

				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={() => {
						eel?.close_app(input_value)();
					}}
				>
					Close
				</button>

				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={() => {
						eel?.google_search(input_value)();
					}}
				>
					Google Search
				</button>
				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={() => {
						eel?.youtube_search(input_value)();
					}}
				>
					YouTube Search
				</button>
				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={() => {
						eel?.play_music(input_value)();
					}}
				>
					Play Music
				</button>
			</div>
		</div>
	</div>
</div>
