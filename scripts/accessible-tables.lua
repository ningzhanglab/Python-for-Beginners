-- pandas emits an unnamed index corner, or a separate index-name header row.
-- Put the index name in the corner (a generic label only when it is unnamed).
local function label_table(tbl)
  if not tbl.classes:includes('dataframe') then return tbl end
  local rows = tbl.head.rows
  if not rows[1] or not rows[1].cells[1] then return tbl end
  if #rows == 2 and #rows[1].cells == #rows[2].cells then
    local name_row = rows[2]
    local only_index_name = pandoc.utils.stringify(name_row.cells[1].contents) ~= ''
    for index = 2, #name_row.cells do
      if pandoc.utils.stringify(name_row.cells[index].contents) ~= '' then
        only_index_name = false
      end
    end
    if only_index_name then
      local column_name = pandoc.utils.stringify(rows[1].cells[1].contents)
      if column_name == '' then
        rows[1].cells[1].contents = name_row.cells[1].contents
      else
        local index_name = pandoc.utils.stringify(name_row.cells[1].contents)
        rows[1].cells[1].contents = {pandoc.Plain({pandoc.Str('Rows: ' .. index_name .. '; columns: ' .. column_name)})}
      end
      rows:remove(2)
    end
  end
  if pandoc.utils.stringify(rows[1].cells[1].contents) == '' then
    rows[1].cells[1].contents = {pandoc.Plain({pandoc.Str('Row label')})}
  end
  return tbl
end

function Table(tbl)
  return label_table(tbl)
end

-- Jupyter's complete HTML table representation is raw at this filter stage.
-- Parse that representation so header edits operate on cells, not on HTML text.
function RawBlock(block)
  if block.format == 'html' and block.text:match('<table[^>]*class="[^"]*dataframe')
      and block.text:match('</table>') then
    return pandoc.read(block.text, 'html'):walk({Table = label_table}).blocks
  end
end
