% rebase('base.tpl', title='Audiobooks', current_page=current_page)

<p>Total: <em>{{totalSpace}}</em>. Free: <em>{{freeSpace}}</em>.</p>

<div class="overflow-hidden border border-gray-200 md:rounded-lg">
  <table class="min-w-full divide-y divide-gray-200">
    <thead class="bg-gray-50">
      <tr>
        <th scope="col" class="px-12 py-3.5 text-sm font-normal text-left text-gray-500">Name</th>
        <th scope="col" class="px-12 py-3.5 text-sm font-normal text-left text-gray-500">Tag</th>
        <th scope="col" class="px-12 py-3.5 text-sm font-normal text-left text-gray-500">Action</th>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200 dark:divide-gray-700">
      % for item in items:
        <tr>
          <td class="px-4 py-4 text-sm font-medium whitespace-nowrap text-gray-800" >{{item["name"]}}</td>
          <td class="px-4 py-4 text-sm font-medium whitespace-nowrap text-gray-700">{{item["tag"]}}</td>
          <td class="px-4 py-4 text-sm font-medium whitespace-nowrap">
            % if item["tag"]:
              <a href="remove/{{ item['tag'] }}">Remove</a>
            % else:
              <a href="add/{{ item['name'] }}">Add</a>
            % end
          </td>
        </tr>
      % end
    </tbody>
  </table>
</div>
