<script lang="ts">
    import clsx from "clsx";

    export let selected: boolean = false;

    let clazz: string | null = null;
    export { clazz as class };

    $: className = clsx(
        "m-1 p-1 rounded-md text-center text-zinc-100",
        selected
            ? "bg-sky-900 ring-sky-900 text-zinc-100"
            : "bg-gray-500 ring-gray-500 text-zinc-200 hover:ring-gray-400",
        clazz,
        "hover:cursor-pointer ring-1",
    );

    $: console.log(className);
</script>

<div on:click class={className}>
    <slot/>
</div>