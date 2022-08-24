<script lang="ts">
    import clsx from "clsx";

    export let selected: boolean = false;
    export let colorBase: string = "gray-500";
    export let colorSelected: string = "sky-900";

    let clazz: string | null = null;
    export { clazz as class };

    $: className = clsx(
        "m-1 p-1 rounded-md text-center text-zinc-100",
        selected
        ? `bg-${colorSelected} ring-${colorSelected} text-zinc-100 hover:ring-gray-400`
        : `bg-${colorBase} ring-${colorBase} text-zinc-200 hover:ring-gray-400`,
        clazz,
    );

    $: console.log(className);
</script>

<button on:click class={className}>
    <slot/>
</button>