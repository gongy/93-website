<script lang="ts">
    import clsx from "clsx";
import { LogInIcon } from "svelte-feather-icons";
    import Button from "./Button.svelte";

    const people = ["ak", "dansun", "cjs", "rgong", "jlee", "bwu"];

    let selected: string = "";
    $: console.log(selected);
</script>

<div class="m-1 p-2 bg-gray-600 rounded-md">
    <div class="text-zinc-100 text-center">I am</div>
    <div
        class="grid grid-cols-1 2xs:grid-cols-2 xs:grid-cols-3 sm:grid-cols-6 p-2"
    >
        {#each people as person}
            <Button
                selected={selected === person}
                on:click={() => {
                    selected = selected === person ? "" : person;
                }}
            >{person}</Button>
        {/each}
    </div>
</div>
<div class="grid grid-cols-2">
    <div class="m-1 p-2 bg-gray-600 rounded-md">
        <div class="py-1 text-zinc-100 text-center">Washer</div>
        <div class="py-1 text-zinc-400 text-center">Status: free</div>
        <div class="py-1 flex justify-center">
            <Button class="p-1 flex-grow" on:click={() => {console.log("claim");}}>Claim 1 hour</Button>
        </div>
    </div>
    <div class="m-1 p-2 bg-gray-600 rounded-md">
        <div class="py-1 text-zinc-100 text-center">Dryer</div>
        <div class="py-1 text-zinc-400 text-center">Status: free</div>
        <div class="py-1 flex justify-center">
            <Button class="p-1 flex-grow" on:click={() => {console.log("claim");}}>Claim 1 hour</Button>
        </div>
    </div>
</div>
