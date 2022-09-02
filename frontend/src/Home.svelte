<script lang="ts">
    import { useSWR } from "sswr";
  
    const { data: rows, revalidate } = useSWR("https://gongy-93-fastapi.modal.run/home");
  </script>
  
  <div class="m-1 p-2 bg-gray-600 rounded-md">
    <div class="text-center text-zinc-100 py-2">
        Soon you can see who's home!
    </div>
    <div class="h-7 animate-pulse bg-gray-400 rounded-sm my-2 mx-1"/>
    <div class="h-7 animate-pulse bg-gray-400 rounded-sm my-2 mx-1"/>
  </div>