% rebase('base.tpl', title='Audiobooks')

<div class="mb-10 text-right">
  <div class="stats stats-horizontal shadow">

    <div class="stat">
      <div class="stat-title">Free</div>
      <div class="stat-value">{{ freeSpace }}</div>
      <div class="stat-desc">{{ freePercent }} %</div>
    </div>

    <div class="stat">
      <div class="stat-title">Used</div>
      <div class="stat-value">{{ usedSpace }}</div>
      <div class="stat-desc">{{ usedPercent }} %</div>
    </div>

    <div class="stat">
      <div class="stat-title">Total</div>
      <div class="stat-value">{{ totalSpace }}</div>
      <div class="stat-desc"></div>
    </div>

  </div>
</div>

<div class="overflow-x-auto border border-gray-200 md:rounded-lg">
  <table class="table table-zebra">
    <thead class="bg-gray-50">
      <tr>
        <th>Name</th>
        <th>Size</th>
        <th>Tag</th>
        <th>&nbsp;</th>
      </tr>
    </thead>
    <tbody>
      % for item in items:
        <tr>
          <td>{{item["name"]}}</td>
          <td>{{sizeof_fmt(item["size"], 'B')}}</td>
          <td>
            % if item["tag"] is not None:
              <div class="badge badge-accent">{{ item["tag"] }}</div>
            % end
          </td>
          <td>
            % if item["tag"]:
              <a href="{{ url('play', tag=item['tag']) }}" class="btn btn-accent btn-xs">Play</a>
              <a href="{{ url('play_from_start', tag=item['tag']) }}" class="btn btn-accent btn-xs">Play from Start</a>
              <a href="{{ url('removeTag', tag=item['tag']) }}" class="btn btn-neutral btn-xs">Clear Tag</a>
            % else:
              <a href="{{ url('addTag', name=item['name']) }}" class="btn btn-neutral btn-xs">Add Tag</a>
            % end
          </td>
        </tr>
      % end
    </tbody>
  </table>
</div>
