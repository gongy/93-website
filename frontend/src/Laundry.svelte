<script lang="ts">
    import Button from "./Button.svelte";

    const people = [
        {name: "ak", color: "bg-pink-900 ring-pink-900"},
        {name: "dansun", color: "bg-purple-900 ring-purple-900"},
        {name: "cjs", color: "bg-indigo-900 ring-indigo-900"},
        {name: "rgong", color: "bg-sky-900 ring-sky-900"},
        {name: "jlee", color: "bg-teal-900 ring-teal-900"},
        {name: "bwu", color: "bg-green-900 ring-green-900"},
    ];

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
                selected={selected === person.name}
                selectedClass={"bg-gray-700 ring-gray-700"}
                on:click={() => {
                    selected = selected === person.name ? "" : person.name;
                }}
            >{person.name}</Button>
        {/each}
    </div>
</div>
<div class="grid grid-cols-2">
    <div class="m-1 p-2 bg-gray-600 rounded-md">
        <div class="py-1 text-zinc-100 text-center">Washer</div>
        <div class="py-1 text-zinc-400 text-center">Status: free</div>
        <div class="py-1 flex justify-center">
            <Button class="flex-grow" on:click={() => {console.log("claim");}}>Claim 1 hour</Button>
        </div>
    </div>
    <div class="m-1 p-2 bg-gray-600 rounded-md">
        <div class="py-1 text-zinc-100 text-center">Dryer</div>
        <div class="py-1 text-zinc-400 text-center">Status: free</div>
        <div class="py-1 flex justify-center">
            <Button class="flex-grow" on:click={() => {console.log("claim");}}>Claim 1 hour</Button>
        </div>
    </div>
</div>
