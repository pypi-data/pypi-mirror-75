// Escape regex key characters
RegExp.escape = function(string) {
  return string.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')
};

// Toggle (De)compression Class
function toggleCompression(el, compress=null) {
    if(compress !== null) {
        if(compress === true) {
            el.classList.replace('decompressed', 'compressed');
        } else {
            el.classList.replace('compressed', 'decompressed');
        }
    } else {
        el.classList.toggle('compressed');
        el.classList.toggle('decompressed');
    }
}

// Toggle Display None/Block
function toggleShowHide(el, hide=null) {
   if(hide !== null) {
       if(hide === true) {
           el.classList.replace('show', 'hide');
       } else {
           el.classList.replace('hide', 'show');
       }
   } else {
       el.classList.toggle('hide');
       el.classList.toggle('show');
   }
}

// Hide/Show Filters Container
function handleShowFilter(filters_btn) {
    filters = document.getElementById('filters');
    toggleCompression(filters);
    filters_btn.textContent = filters.classList.contains('decompressed') ? "Hide Filters" : "Show Filters";
}

/* Log Content Handles */
// Expand Subsequent Logs With Same Depth
function expandLogs(log_entry) {
    log_entry.classList.add('expanded');
    exp_btn = log_entry.querySelector('.exp-btn');
    exp_btn.classList.replace('hide-logs', 'show-logs');
    depth = log_entry.getAttribute('aria-label');
    // For each sibling...
    for(var i=log_entry.nextElementSibling; i!==null; i=i.nextElementSibling) {
        if(Number(i.getAttribute('aria-label')) == (Number(depth) + 1)) {
            // If the depth of this log entry is the same as the original entry, show it.
            toggleShowHide(i, hide=false);
        }
        else if (Number(i.getAttribute('aria-label')) > (Number(depth) + 1)) {
            // If the depth is greater, it is a child entry of another log. Just skip it.
            continue;
        }
        else {
            // The depth of this entry belongs to a parent depth. Stop looping.
            break;
        }
    }
}
// Collapse Subsequent Logs Of Greater Depth
function collapseLogs(log_entry) {
    log_entry.classList.remove('expanded');
    exp_btn = log_entry.querySelector('.exp-btn');
    if(exp_btn) {
        // If the entry has child entries, toggle the arrow of the exp btn.
        exp_btn.classList.replace('show-logs', 'hide-logs');
    }
    depth = log_entry.getAttribute('aria-label');
    // For each sibling...
    for(var i=log_entry.nextElementSibling; i!==null; i=i.nextElementSibling) {
        if(depth < i.getAttribute('aria-label')) {
            // If the depth of the original entry is less than this one, then this is a
            // descendant entry. Hide it.
            toggleShowHide(i, hide=true);
            exp_btn = i.querySelector('.exp-btn');
            if(exp_btn) {
                // If the exp btn exists, set the arrow to hide.
                exp_btn.classList.replace('show-logs', 'hide-logs');
            }
        }
        else {
            // This entry belongs to a parent depth. Stop looping.
            break;
        }
    }
}

// Toggle Log Expansion
function toggleExpLogs(log_entry_id) {
    log_entry = document.getElementById(log_entry_id);
    if(!log_entry_id) {
        return;
    }
    if(log_entry.classList.contains('expanded')) {
        collapseLogs(log_entry);
    }
    else {
        expandLogs(log_entry);
    }
}

// Show/Hide Log Message/Info Block And Highlight Button Text
function handleLogContent(btn, block_id, hide=null) {
    block = document.getElementById(block_id);
    toggleShowHide(block, hide);
    if(hide === true) {
        btn.classList.remove('bold');
    } else if(hide === false) {
        btn.classList.add('bold');
    } else {
        btn.classList.toggle('bold');
    }
}

// Handle Code Blocks
function showCode(file_id, file_name, line_num) {
    // Show the code blocks panel.
    code_blocks = document.querySelector('#code-blocks');
    code_blocks.classList.replace('hide', 'show');

    // Get the code block div and show it.
    code_block = document.querySelector('#'+file_id);
    code_block.classList.replace('hide', 'show');

    // Get the code block object tag and scroll it to the top of the panel.
    code = code_block.querySelector('.code');
    code_blocks.scrollTo({top: code_block.offsetTop, behavior: 'smooth'});

    // Send a message to the object frame to scroll to the line number.
    if(code.contentDocument && code.contentDocument.documentElement.innerText == "") {
        // If frame has not yet loaded...
        code.onload = function() {
            code.contentWindow.postMessage(line_num.toString(), "*");
        };
    } else {
        // If frame has loaded already...
        code.contentWindow.postMessage(line_num.toString(), "*");
    }
}

function hideCode(file_id) {
    // Hide the code block div.
    code_block = document.querySelector('#'+file_id);
    code_block.classList.replace('show', 'hide');

    // Clear the inner HTML of the object frame.
    code = code_block.querySelector('.code');
    if(code.contentDocument) {
        // If frame has already loaded, clear it.
        code.contentDocument.documentElement.innerHTML = "";
    }

    // If there are no more code blocks, hide the panel.
    code_blocks = document.querySelector('#code-blocks');
    if(code_blocks.querySelectorAll('.show').length <= 0) {
        // If no code blocks are left, close side panel.
        code_blocks.classList.replace('show', 'hide');
    }
}

// Reset All Log Blocks And Entries To Original State
function resetLogBlocks() {
    // Get all message and info log blocks.
    blocks = document.querySelectorAll('.log-block');
    blocks.forEach((block) => {
        log_entry = block.parentElement.parentElement;
        // Close the log block.
        if(block.classList.contains('info-block')) {
            btn = log_entry.querySelector('.info-btn > button');
            handleLogContent(btn, block.id, compress=true);
        } else if(block.classList.contains('msg-block')) {
            btn = log_entry.querySelector('.msg-btn > button');
            handleLogContent(btn, block.id, compress=true);
        }

        // Make background transparent in case it was highlighted by search.
        block.firstElementChild.style.backgroundColor = 'transparent';
    })

    // Hide all log entries and reset the exp btn for each entry.
    log_entries = document.querySelectorAll('.log-entry');
    log_entries.forEach((log_entry) => {
        exp_btn = log_entry.querySelector('.exp-btn');
        if(exp_btn) {
            exp_btn.classList.replace('show-logs', 'hide-logs');
            collapseLogs(log_entry);
        }
    })

    // Clear search results text.
    search_results = document.querySelector('#search-count');
    search_results.innerHTML = '';
}

// Regex Calculator
function searchRegex(text) {
    var wwo = document.querySelector('#search-whole-word');
    var regex = document.querySelector('#search-regex');
    var mc = document.querySelector('#search-match-case');

    // Prevent the text from inserting unwanted regex characters.
    var expr = regex.checked ? text : RegExp.escape(text);
    if(wwo.checked) {
        expr = `\\b${expr}\\b`;  // whole word only
    }
    var params = 'm';  // multi-line search option
    if(!mc.checked) {
        params += 'i';  // case insensitive
    }
    return new RegExp(expr, params);
}

// Process search request.
function processSearch(text, tag_toggled=false) {
    // Reset everything to reduce noise of search.
    resetLogBlocks();
    var include_msg_block = document.querySelector('#search-in-msg');
    var include_code_block = document.querySelector('#search-in-code');
    var include_info_block = document.querySelector('#search-in-info');
    var regex = searchRegex(text);
    var total_num_results = 0;  // Total searches found, but not necessarily shown.
    var shown_num_results = 0;  // Total searches shown.

    log_blocks = document.querySelectorAll('.log-block');
    // For every log block...
    for(var x=0; x < log_blocks.length; x++) {
        if(log_blocks[x].textContent.match(regex)) {
            // If a match occurs...
            total_num_results += 1;
            found = log_blocks[x];
            log_entry = found.parentElement.parentElement;
            if(include_info_block.checked && found.classList.contains('info-block')) {
                btn = log_entry.querySelector('.info-btn > button');
            } else if(include_msg_block.checked && found.classList.contains('msg-block')) {
                btn = log_entry.querySelector('.msg-btn > button');
            } else {
                continue;
            }
            if(log_entry.style.display !== 'none') {
                shown_num_results += 1;
                toggleShowHide(log_entry, hide=false);
            } else {
                continue;
            }

            // If the match has parent entries, expand them.
            cur_depth = Number(log_entry.getAttribute('aria-label'));  // Depth of match
            for(var j=log_entry.previousElementSibling; j !== null; j=j.previousElementSibling) {
                depth = Number(j.getAttribute('aria-label'));  // Depth of previous sibling
                if(depth < cur_depth) {
                    // The previous sibling is an ancestor
                    cur_depth = depth;
                    expandLogs(j);
                } else if (depth <= 0) {
                    break;  // No more ancestors. Stop looping.
                }
            }
            // Simulate a click to show the log block.
            handleLogContent(btn, found.id, compress=false);

            // Highlight the log block to show that it matched a search.
            found.firstElementChild.style.backgroundColor = 'rgba(0, 255, 0, 0.1)';
        }
    }

    // Display numbers of matched and shown entries of search.
    search_results = document.querySelector('#search-count');
    search_results.innerHTML = total_num_results + ' total results match "' + text + '".<br/>' + shown_num_results + ' results shown.';
}

// Search Log Entries By Message Blocks, Info Blocks, Whole-Word Only,
// Regular Expression, And/Or Match By Case.
function search(search_el_id, tag_toggled=false) {
    search_el = document.querySelector('#'+search_el_id);
    search_results = document.querySelector('#search-count');

    text = search_el.value;
    if(text.length == 0) {
        // Search text is empty.
        if(!tag_toggled) {
            // Don't ignore. Display message to type something.
            search_results.innerHTML = 'Type something to search.';
        }
        // Ignore.
        return;
    }

    // Call search engine.
    search_results.innerHTML = 'Searching...';
    setTimeout(function () { processSearch(text, tag_toggled); }, 120);
}

// Search When Input Has Focus And Enter Key Is Selected.
function searchOnEnter(event, search_el_id) {
    if(event.keyCode === 13) {
        search(search_el_id);
    }
}

// Hide/Show By Log Tag
function handleLogTagFilter(filter) {
    log_tag = filter.querySelector('input[type="checkbox"]');
    log_entries = document.querySelectorAll('.log-entry');
    display = log_tag.checked ? 'block' : 'none';
    triggered_depth = -1;
    triggered = false;
    log_entries.forEach((log_entry) => {
        var name = log_entry.getAttribute('aria-valuetext');  // This tag name.
        if(triggered) {
            var depth = log_entry.getAttribute('aria-label');  // This depth.
            if(Number(depth) > triggered_depth) {
                // If this depth is greater than the triggered depth, then it is a
                // descendant entry of the entry that was shown/hidden. So also
                // show/hide this, respectively.
                log_entry.style.display = display;
            } else {
                // This depth is less than the ancestor depth that triggered all child
                // logs to show/hide, so it is not affected. Lift the trigger.
                triggered = false;
            }
        }
        if(name !== null && name == log_tag.id) {
           // If this matches the log tag...
           log_entry.style.display = display;  // Show/Hide the entry.

           // Set trigger to indicate that all future siblings should be shown/hidden
           // until the depth matches this depth. This means all children entries of
           // an entry matching the log tag filter will be shown/hidden with its parent.
           if(!triggered) {
               triggered = true;
               triggered_depth = Number(log_entry.getAttribute('aria-label'));
           }
       }
    })
}
