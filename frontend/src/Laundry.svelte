<script lang="ts">
    import Button from "./Button.svelte";
    import { useSWR } from "sswr";
    import { Trash2Icon } from "svelte-feather-icons";
    import { userToken } from "./stores";

    import jwt_decode from "jwt-decode";
    import { formatEnd } from "./utils";

    const people = [
        {name: "ak", color: "bg-pink-900 ring-pink-900"},
        {name: "dansun", color: "bg-purple-900 ring-purple-900"},
        {name: "cjs", color: "bg-indigo-900 ring-indigo-900"},
        {name: "rgong", color: "bg-sky-900 ring-sky-900"},
        {name: "jlee", color: "bg-teal-900 ring-teal-900"},
        {name: "bwu", color: "bg-green-900 ring-green-900"},
    ];

    $: if ($userToken) {
        const name = (jwt_decode($userToken) as any).given_name.toLowerCase() || ".";
        if (!selected) {
            const r = people.map((p) => p.name).filter((n) => n[0] == name[0]);
            if (r.length > 0) selected = r[0];
        }
    }


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
            <Button class="grow" on:click={async () => { await sendLaundryUpdate("washer", selected, 3600); revalidate()}}>Claim 1 hour</Button>
            <Button class="grow-0 flex items-center justify-center" on:click={async () => { await sendLaundryUpdate("washer", selected, -1000); revalidate(); }}>
                <Trash2Icon class="w-4 h-4 m-1"/>
            </Button>
        </div>
    </div>
    <div class="flex flex-col justify-between m-1 p-2 bg-gray-600 rounded-md">
        <div class="py-1 text-zinc-100 text-center">Dryer</div>
        <div class="py-1 text-zinc-100 text-center">
            {dryerName} {dryerEnd ? `(${formatEnd(dryerEnd)} left)` : ""}
        </div>
        <div class="py-1 flex justify-center">
            <Button class="grow" on:click={async () => { await sendLaundryUpdate("dryer", selected, 3600); revalidate(); }}>Claim 1 hour</Button>
            <Button class="grow-0 flex items-center justify-center" on:click={async () => { await sendLaundryUpdate("dryer", selected, -1000); revalidate(); }}>
                <Trash2Icon class="w-4 h-4 m-1"/>
            </Button>
        </div>
    </div>
</div>
