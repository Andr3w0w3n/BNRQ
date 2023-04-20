import nuke
import sys

#not needed as of yet, but imported just in case
import logging

#Exit codes with constants
EXIT_NO_WRITE_NODE = 104
EXIT_UNKNOWN_RENDER_ERROR = 206
EXIT_RENDER_CANCELLED = 200
EXIT_RENDER_ERROR = 201
EXIT_RENDER_MEMORY_ERROR = 202
EXIT_RENDER_PROGRESS_ABORTED = 203
EXIT_RENDER_LICENSE_ERROR = 204
EXIT_RENDER_USER_ABORT = 205
EXIT_NO_SCRIPT = 404


def find_write_node(write_node_name = "Write1"):
    
    """
    Find and return the Write node with the given name.

    Args:
        write_node_name (str): The name of the Write node to search for.

    Returns:
        nuke.Node: The Write node with the given name

    Raises:
        (AttributeError): If the node with the given name is not a Write node.
    """

    try:
        return nuke.toNode(write_node_name)
    except AttributeError as e:
        exit(EXIT_NO_WRITE_NODE)


def render_script(ns, wn):

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

    Returns:
        None.
    """

    error_codes = {
        nuke.RenderCancelled: EXIT_RENDER_CANCELLED,
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


def main(nuke_script = nuke.Root()):
    
    """
    Find write node and render script with the found write node.

    Args:
        nuke_script (nuke.Script): the Nuke script to render

    Raises:
        None.

    Returns:
        None.
    """

    #setting the logging [not being used]
    #logging.basicConfig(level = logging.ERROR)

    write_node = find_write_node()
    
    render_script(nuke_script, write_node)

    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        try:
            root = nuke.Root()
            main()
        except NameError:
            sys.exit(EXIT_NO_SCRIPT)
    nuke_script_arg = sys.argv[1]
    main(nuke_script_arg)