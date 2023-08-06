
# DB Logging  
  
## Summary  
DB Logging is a Python logging utility that creates tag-based log messages in a SQLite database. This is a power
mechanism for logging because the logs persist in a very easily queryable log file. Additionally, an HTML generator
is included to parse the DB file and create a beautiful rendering of the log entries.
  
## Installation  
  
There are two methods for installing this module:  
  
1. `pip install dblogging`
2. Clone from Gitlab.  

## Usage Guide

Follow these steps to get started. Note the tips for extra pointers! See the *examples* folder for examples of using 
the logger.

### Create The Custom Log Tags
  
The derived LogTags class MUST include at least these two properties: _default_ and _critical_. This is
because the logging functions need a default log tag in case the log method was not explicitly given one by the
programmer. The _critical_ tag is only used by `log_exception()` and cannot be overridden. While these properties
exist, their values can be overridden. 

Each log tag requires three values: a `name`, a `value`, and an `html_color` _(not required)_. The idea is to be able
to filter code by group names or by a threshold of some sort to sift out other noise within the log file.

* The _name_ denotes a group name to which log entries will belong, such as a severity like _DEBUG_ or a layer of code
 such as _API_.
* The _value_ is an integer that places a value to the tag such as severity or level within a layer of code. 
* The _html_color_ is optional. It is the color used when generating the HTML file with the `HtmlGenerator()`.

There are two easy ways to create custom log tags.  
  
1. Import LogTagTemplate to customize the _default_ and _critical_ log tags. 
```  
from dblogging.config import LogTagTemplate, LogTag  


class LogTags(LogTagTemplate):  
    # default and critical must be defined. 
    default = LogTag( 
        name='Standard', 
        value=0, 
        html_color='cyan' 
    )  
    critical = LogTag( 
        name='Critical', 
        value=90, 
        html_color='red' 
    )  
    # custom tags below 
    DAL = LogTag( 
        name='Data Access Layer', 
        value=10, 
        html_color='#0F0'  # green 
    )
```  

2. Import LogTags to define just the custom tags. The _default_ and _critical_ tags are already defined.  
```  
from dblogging.config import LogTags as _LogTags, LogTag
  
  
class LogTags(_LogTags):  
    # custom tags below 
    DAL = LogTag( 
        name='Data Access Layer', 
        value=10, 
        html_color='#0F0'  # green 
    )
```
   
### Writing Logs

When `Logger()` is called it is disabled until `start()` is called. This allows the program to explicitly decide when
logging is enabled and how. Prior to begin logging be sure to consider setting these variables:

* `log_path`: This is the absolute path to the SQLite log file with or without the _.db_ extension. The parent
folder must exist and the log file must not already exist. If this variable is not set prior to `start()` then logs
will only be directed to _stdout_ via `print()`.
* `log_tags`: If not defined prior to `start()` then the default `dblogging.config.LogTags` is used. See the section
above for more details on customizing the log tags. 
* `date_format`: When `print()` is called this date format is used to log the entry to _stdout_. If logging to the
database as well then this format will NOT apply. The default value is `%Y/%m/%d %H:%M:%S`.

When `start()` is called the logger is enabled and, if and only if `log_path` is defined, the SQLite database is
initialized with a _log_tags_ and _log_entries_ table. The _log_tags_ table can only be populated once and is
populated on `start()` with the log tag information. If the log tags are redefined later in the program it will not
be persisted into the database by the logger and would require the programmer's intervention.

When logging message the logger grabs these few items about the log entry:
* _file path_: The absolute path to the function, or caller, referenced in the call stack of the log entry.
* _function name_: The name of the function, or caller, referenced in the call stack of the log entry.
* _line number_: The line number of the function, or caller, referenced in the call stack of the log entry.
* _message_: The log message.
* _log tag_: The log tag the accompanies the log entry. The logger uses this tag to decide if the message should or
should not be logged based on the currently defined log rule. See _Setting Log Rules_ below for more details.
* _thread information_: The thread id and name of the call stack.

Here are all of the logging methods and how they work.

* `log()`: Logs a message with a log tag.
    * `msg`: The log message. Required.
    * `log_tag`: Default is the `default` tag. 
    * `num_prev_callers`: This is the caller within the call stack to reference. The logger dynamically retrieves
     data about the caller based on this value. Default is 0.
* `log_exception()`: Logs the exception with the `critical` log tag. This cannot be overridden. If `generate()` is
 not used, then be sure to include this in an except clause at the very least.
* `log_method()`: Not really useful to the programmer. Rather than dynamically retrieving data about a caller like
 `log()` does, this explicitly logs data about the caller passed to the method.
    * `func`: A callable function.
    * `msg`: The log message.
    * `log_tag`: The log tag that logs the message. Defaults to the default tag.
    * `returning`: If `True`, reference the last line of the method, otherwise the first.
* `generate()`: This is the context manager that wraps the execution of the given code block in a `try/except/finally` 
clause. It accepts a `format_generator` parameter that, if defined, will generate the log file in the given format. If 
it is not given, then the database file will still persist if a `log_path` is given prior to starting the logger.
    * `format_generator`: Either a string or callable generator class. Right now the only acceptable string value is
    _html_, which references the built-in HTML log generator. The programmer can design a custom generator that
    parses the SQLite database entries to output the desired format. The custom generator **MUST** have an 
    `__init__(self)` method that accepts no arguments and a `generate()` method that may accept arguments. 
    * `kwargs`: Supplementary keywords can be passed to the `generate()` function. 
* `wrap_func()`: A function wrapper that logs the inputs and outputs of the function. The function may not be a
generator function or yield anything to the caller. `staticmethod` and `classmethods` are supported. This method
accepts a list of regular expressions to map to input parameter names whose values should be masked. Output values
can only be entirely masked or not at all due to the complexity and time to parse the output to decide what to mask. 
The inputs and outputs are logged with `jsonpickle` and only logs picklable objects to avoid errors with a max depth
of 3 (meaning nested iterable objects are only logged up to 3 iterations).
    * `log_tag`: The log tag to use to log the input and output messages. If not given, then the `default` tag is used.
    * `mask_input_regexes`: A list of regular expressions that map to input parameter names whose values should be
    masked.
    * `mask_output`: If `True`, then the output message is simply "Output is masked." Otherwise, the output is given
    in the message.  
    * `is_static_or_classmethod`: Must be `True` when using the `staticmethod` or `classmethod` wrappers. 
* `wrap_class()`: Applies the `wrap_func()` wrapper to all callable members of a class that do not start with two
underscores (__). This method automatically detects `staticmethod` and `classmethod` attributes. A single regular
expression can be given to describe those methods that should NOT be wrapped. Just like `wrap_func()`, input parameter 
values and output values can be masked. However, these are globally applicable values, so every method will apply these
values. It is more efficient to define the input masking rules per method because the logger does not attempt to parse 
the inputs if nothing is defined. `wrap_func()` overrides `wrap_class()`, so it can be placed on a method that may 
require a different log tag or must have an input or output masked.
    * `log_tag`: The log tag to use to log the input and output messages. If not given, then the `default` tag is used.
    * `func_regex_exclude`: The regular expression describing the functions to not wrap.
    * `mask_input_regexes`: A list of regular expressions that map to input parameter names whose values should be
    masked.
    * `mask_output`: If `True`, then the output message is simply "Output is masked." Otherwise, the output is given
    in the message. 

### Setting Log Rules

When enabled, log rules can be created on the fly to manage which logs are actually committed to the console and/or to
the database. Here are the parameters to `set_rule()`:

* `mode`: The mode, a string value, is the target for log entries. There are four possible values: 
    * "console": Only commit log entries that satisfy the rule via `print()`.
    * "persistence": Only commit log entries that satisfy the rule to the database.
    * "all": Commit log entries that satisfy the rule both via `print()` and to the database.
    * "current": Default. Commit log entries that satisfy the rule using the current mode.
* `log_tag`: Used to log `why`. If not given the _default_ tag is used.
* `min_tag_value`: The minimum log tag value, inclusive, that must accompany a log entry to be committed. 
* `blacklist_tag_names`: A list of log tag names that whose log entries will NOT be committed.
* `blacklist_function`: A `lambda` function that customizes the wanted behavior. This function MUST accept only one
parameter, _x_, which is the log tag used to commit a log entry.
* `reset`: Resets the rule to the original state, except the mode.
* `why`: The reason why the rule is being set.

If none of `min_tag_value`, `blacklist_tag_names`, `blacklist_function`, or `reset` is defined, then all log entries
will be logged via the `mode` given. The order of execution of these functions is as follows:
1. `blacklist_function`
2. `min_tag_value`
3. `blacklist_tag_names`
4. `reset`
5. Allow all log entries. This is the same as `reset`, only a different message is logged.

Logs can also be disabled. This option is only available as a context manager, meaning the `with` statement is
required. Be cautious when using this option because all logs in the context will be disabled. Upon exit of the 
context the logger will switch the disabled rule back to its original state. If `logger.start()` was never called,
then it would not be enabled when the context exits. Otherwise the logger would be re-enabled. If an exception was
thrown in the context and the logger was started, then the exception will be re-raised by the logger and logged. 

### Generating The HTML File

> Refer to **dblogging/examples/logs/example.html** in this repository to view the output files.

This type of log file generation can be very useful for having a nice visual into the logs. While having a database to
query is very nice, having a more friendly output that you can render in your browser is very handy. However, proceed 
with caution as very large log files can take a very long time to render. To help with this, the `HtmlGenerator()` has 
a couple of parameters that can help.

The `HtmlGenerator()` accepts these parameters:

* `log_file`: The absolute path to the _.db_ log file. If using the `generate()` method, the logger handles this for 
you. 
* `title`: The title of the HTML page. 
* `include_code`: If `True`, each raw code file referenced by the log entries will be compiled to HTML. To increase 
performance and save space, the output HTML file makes an `<object>` reference to these files so each code file is not 
a) included directly in the output file and b) not duplicated in the output. To preserve reference integrity, each code
file's HTML is named according to the ``uuid.uuid3()`` hash of the absolute path to the file. If `False`, raw code is 
not included with the output.
* `datetime_range`: Must be a `Tuple` of length 2 where the first value is the starting datetime and the second is the
ending datetime. If either is undesired, then the value must be set explicitly to `None` (i.e. `(None, today)` for just
and end date of today). The values must be `datetime` objects. This is particularly useful for reducing the size and 
narrowing the target of the desired logs. 
* `exclude_files`: A list of regular expressions that describe the list of code files that should not be compiled and 
referenced by the output. If `include_code=False`, this parameter is moot.
