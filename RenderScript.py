import nuke
import sys
import datetime

#not needed as of yet, but imported just in case
import logging

#Exit codes with constants
EXIT_NO_WRITE_NODE = 104
EXIT_RENDER_CANCELLED = 200
EXIT_RENDER_ERROR = 201
EXIT_RENDER_MEMORY_ERROR = 202
EXIT_RENDER_PROGRESS_ABORTED = 203
EXIT_RENDER_LICENSE_ERROR = 204
EXIT_RENDER_USER_ABORT = 205
EXIT_UNKNOWN_RENDER_ERROR = 206
EXIT_NO_SCRIPT = 404

sys.stdout = sys.__stdout__

def find_write_node(write_node_name):
    """
    Find and return the Write node with the given name.

    Args:
        write_node_name (str): The name of the Write node to search for.

    Returns:
        nuke.Node: The node with the given name (At this point, it could not be a write node)

    Raises:
        (ValueError): If the node with the given name is not in the script.
    """

    try:
        write_node_temp = nuke.toNode(write_node_name)
        if write_node_temp is None:
            raise ValueError()
        return write_node_temp
    except ValueError as e:
        exit(EXIT_NO_WRITE_NODE)


def render_script(wn):
    """
    Render the given Nuke script using the specified write node.

    Args:
        ns (nuke.Node): The Nuke script to render.
        wn (nuke.Node): The write node to use for rendering.

    Raises:
        nuke.RenderCancelled: If the render was cancelled by the user.
        nuke.RenderError: If a general render error occurred.
        nuke.RenderMemoryError: If the render ran out of memory.
        nuke.RenderProgressAborted: If the render was aborted.
        nuke.RenderLicenseError: If there was a problem with the Nuke license.
        nuke.RenderUserAbort: If the render was aborted by the user.
    """

    """
    #these errors are wrong, have to look into proper error types
    error_codes = {
        nuke.ExecuteAborted: EXIT_RENDER_CANCELLED,
        nuke.RenderError: EXIT_RENDER_ERROR,
        nuke.RenderMemoryError: EXIT_RENDER_MEMORY_ERROR,
        nuke.RenderProgressAborted: EXIT_RENDER_PROGRESS_ABORTED,
        nuke.RenderLicenseError: EXIT_RENDER_LICENSE_ERROR,
        nuke.RenderUserAbort: EXIT_RENDER_USER_ABORT,
    }

    try:
        nuke.execute(wn, start = ns.firstFrame(), end = ns.lastFrame(), incr = 1)
    except Exception as e:
        if type(e) in error_codes:
            sys.exit(error_codes[type(e)])
        else:
            print("An unknown render error occurred.")
            sys.exit(206)
    """
    try:
        nuke.execute(wn, start = nuke.root().firstFrame(), end = nuke.root().lastFrame())
    except BaseException as e:
        sys.exit(EXIT_RENDER_ERROR)


def main(nuke_script = nuke.Root(), write_node_name = "Write1"):
    """
    Find write node and render script with the found write node.

    Args:
        nuke_script (nuke.Script): the Nuke script to render
        write_node_name (str): the name of the write node that the user selected,
                defaults to "Write1".
    """
    #setting the logging [not being used]
    #logging.basicConfig(level = logging.ERROR)
    nuke.scriptOpen(nuke_script)
    write_node = find_write_node(write_node_name)
    
    render_script(write_node)

    sys.exit(0)


if __name__ == "__main__":
    """
    sys.stdout = open("V:/NUKE Addons - KEEP/Created Scripts/RenderQ/NukeLog.txt", "w")
    print("-----------------------------------------")
    print(f"Testing {nuke.root().name()}: {str(datetime.datetime.now())}" )
    print("We made it into the if __name__!")
    print("The argument passed in is: " + sys.argv[1])
    """
    if len(sys.argv) < 3:
        try:
            root = nuke.Root()
            main()
        except NameError:
            sys.exit(EXIT_NO_SCRIPT)
    nuke_script_arg = sys.argv[1]
    write_node_name_arg = sys.argv[2]
    main(nuke_script_arg, write_node_name_arg)