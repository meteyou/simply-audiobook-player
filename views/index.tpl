<html>
<head></head>
<body>
  <h1>Simply Audiobook Player</h1>
  <p>Total memory: <em>{{totalMem}}</em>. Free memory: <em>{{freeMem}}</em>.</p>
  <table>
  % for item in items:
    <tr>
      <td><p>{{item["name"]}}</p></td>
      <td><p>{{item["tag"]}}</p></td>
      <td>
        % if item["tag"]:
          <a href="remove/{{item["tag"]}}">Remove</a>
        % else:
          <a href="add/{{item["name"]}}">Add</a>
        % end
      </td>
    </tr>
  % end
  </table>
</body>
</html>
