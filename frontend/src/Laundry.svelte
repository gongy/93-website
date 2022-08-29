<script lang="ts">
    import Button from "./Button.svelte";
    import { useSWR } from "sswr";
    import { formatDistance } from "date-fns";

    const people = [
        {name: "ak", color: "bg-pink-900 ring-pink-900"},
        {name: "dansun", color: "bg-purple-900 ring-purple-900"},
        {name: "cjs", color: "bg-indigo-900 ring-indigo-900"},
        {name: "rgong", color: "bg-sky-900 ring-sky-900"},
        {name: "jlee", color: "bg-teal-900 ring-teal-900"},
        {name: "bwu", color: "bg-green-900 ring-green-900"},
    ];

    let selected: string = "";

    const { data, revalidate } = useSWR("https://gongy-93-fastapi.modal.run/laundry");

    $: console.log(selected);

    let washerName = "...";
    let dryerName = "...";
    let washerEnd = 0.0;
    let dryerEnd = 0.0;

    $: if ($data) {
        const status = $data;

        console.log(status);

        washerEnd = Math.max(...status.map((p: any) => p.washer_end)) * 1000;
        dryerEnd = Math.max(...status.map((p: any) => p.dryer_end)) * 1000;

        if (washerEnd <= utc_ts()) washerEnd = 0.0;
        if (dryerEnd <= utc_ts()) dryerEnd = 0.0;

        if (washerEnd) washerName = status.find((p: any) => p.washer_end * 1000 == washerEnd).name;
        else washerName = "free";

        if (dryerEnd) dryerName = status.find((p: any) => p.dryer_end * 1000 == dryerEnd).name;
        else dryerName = "free";
    }

    function utc_ts() {
        return new Date().getTime();
    }
    
    function formatEnd(t) {
        return formatDistance(
            t,
            utc_ts(),
            {
                includeSeconds: true
            }
        )
    }

    async function sendLaundryUpdate (machine, person, offset) {
		const res = await fetch('https://gongy-93-fastapi.modal.run/claim', {
            method: "POST",
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify({
                machine,
                person,
                offset,
            })
        })
    }
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
    <div class="flex flex-col justify-between m-1 p-2 bg-gray-600 rounded-md">
        <div class="py-1 text-zinc-100 text-center">Washer</div>
        <div class="py-1 text-zinc-100 text-center">
            {washerName} {washerEnd ? `(${formatEnd(washerEnd)} left)` : ""}
        </div>
        <div class="py-1 flex justify-center">
            <Button class="flex-grow" on:click={async () => { await sendLaundryUpdate("washer", selected, 3600); revalidate()}}>Claim 1 hour</Button>
        </div>
    </div>
    <div class="flex flex-col justify-between m-1 p-2 bg-gray-600 rounded-md">
        <div class="py-1 text-zinc-100 text-center">Dryer</div>
        <div class="py-1 text-zinc-100 text-center">
            {dryerName} {dryerEnd ? `(${formatEnd(dryerEnd)} left)` : ""}
        </div>
        <div class="py-1 flex justify-center">
            <Button class="flex-grow" on:click={async () => { await sendLaundryUpdate("dryer", selected, 3600); revalidate(); }}>Claim 1 hour</Button>
        </div>
    </div>
</div>
