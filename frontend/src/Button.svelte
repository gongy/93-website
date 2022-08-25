<script lang="ts">
    import clsx from "clsx";

    export let selected: boolean = false;
    export let selectedClass: string = "bg-sky-900 ring-sky-900";

    let clazz: string | null = null;
    export { clazz as class };

    let className: string = "";
    $: className = clsx(
        "m-1 p-1 rounded-md text-center text-zinc-100",
        clazz,
        "hover:cursor-pointer ring-1", 
        selected
        ? "text-zinc-200 hover:ring-gray-400"
        : "text-zinc-200 hover:ring-gray-400",
        selected
        ? selectedClass
        : "bg-gray-500 ring-gray-500",
    );
</script>

<div on:click class={className}>
    <slot/>
</div>