<script lang="ts">
	let eel = window.eel;
	let WAKE_WORD = ['cygen', 'sajan', 'sizon', 'sahjan', 'silent', 'size', 'sizing', ' and '];
	let input_value = '';
	$: interaction = '';
	$: eel?.web_speak(interaction)();
	eel?.set_host('ws://localhost:8888');
	import { Application } from '@splinetool/runtime';
	import { onMount } from 'svelte';
	onMount(() => {
		// @ts-expect-error html element
		const canvas: HTMLCanvasElement = document.getElementById('canvas3d');
		const app = new Application(canvas);
		app.load('https://prod.spline.design/NNfGHj4gsBiVtyuU/scene.splinecode');
	});

	const speechRecon = () => {
		let speech = '';
		const recApi = window?.webkitSpeechRecognition || window?.SpeechRecognition;

		recApi ? null : alert("SpeechRecognition won't work for you");

		let recorder = new recApi();
		recorder.lang = 'en-IN';
		// rec.continuous = true;
		recorder.interimResults = true;

		recorder.onresult = (e: { results: { transcript: string }[][] }) => {
			speech = Array.from(e.results)
				.map((result) => result[0].transcript)
				.join('');
			console.log(speech);
		};

		recorder.start();

		recorder.addEventListener('end', async () => {
			if (WAKE_WORD.some((word) => speech.toLowerCase().includes(word))) {
				console.log('wake word triggered', speech);
				speech = speech
					.split(' ')
					.filter((word) => !WAKE_WORD.includes(word.toLowerCase()))
					.join(' ')
					.trim();
				speech = speech
					.split(' ')
					.filter((word) => !WAKE_WORD.includes(word.toLowerCase()))
					.join(' ')
					.trim();
				recorder.stop();
				if (speech) {
					interaction = await eel.ask(speech.toLowerCase())();
					speech = '';
					recorder.start();
				} else {
					recorder.start();
				}
			} else {
				recorder.start();
			}
		});
	};
</script>

<div class="inset-0  text-center opacity-90">
	<div class="relative">
		<div
			id="main"
			class="flex items-center justify-center border-b border-blue-700 shadow-blue-600 shadow-md"
		>
			<div class="relative w-[100%]">
				<canvas id="canvas3d" />
				{#if interaction}
					<div
						class="absolute bottom-5 left-0 right-0 bg-black/30 p-2 rounded-lg text-white text-center"
					>
						{interaction}
					</div>
				{/if}
			</div>
		</div>

		<div id="lower_button" class="flex justify-around w-screen ">
			<div>
				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={speechRecon}
				>
					Listen
				</button>
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
				<div class="flex">
					<input
						placeholder="Enter command"
						class="bg-black border-white border rounded-md m-4 p-2 text-white"
						bind:value={input_value}
						on:keydown={async (e) => {
							if (e.key === 'Enter') {
								let temp_input = input_value;
								input_value = '';
								interaction = await eel?.ask(temp_input)();
								// interaction_logs = [...interaction_logs, out];
							}
						}}
					/>
					<button
						class="bg-black border-white border rounded-md m-4 p-2 text-white"
						on:click={async () => (interaction = await eel?.ask(input_value)())}
					>
						Send
					</button>
				</div>
			</div>
			<div class="grid grid-cols-4">
				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={async () => {
						await eel?.llm_chat(input_value)();
						input_value = '';
					}}
				>
					Ask llm
				</button>

				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={async () => {
						interaction = await eel?.generate_image(input_value)();
					}}
				>
					Generate Image
				</button>

				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={async () => {
						interaction = await eel?.realtime_chat(input_value)();
					}}
				>
					Ask Real time llm
				</button>
				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={async () => {
						interaction = await eel?.open_app(input_value)();
					}}
				>
					Open
				</button>

				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={async () => {
						interaction = await eel?.close_app(input_value)();
					}}
				>
					Close
				</button>

				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={async () => {
						interaction = await eel?.google_search(input_value)();
					}}
				>
					Google Search
				</button>
				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={async () => {
						interaction = await eel?.youtube_search(input_value)();
					}}
				>
					YouTube Search
				</button>
				<button
					class="bg-black border-white border rounded-md m-4 p-2 text-white"
					on:click={async () => {
						await eel?.play_music(input_value)();
					}}
				>
					Play Music
				</button>
			</div>
		</div>
	</div>
</div>
