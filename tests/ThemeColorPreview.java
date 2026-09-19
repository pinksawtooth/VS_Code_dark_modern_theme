import java.awt.*;
import java.awt.image.BufferedImage;
import java.nio.file.Path;
import javax.imageio.ImageIO;
import generic.theme.GTheme;

/** Color samples using Ghidra-resolved values; this is not a live GUI capture. */
public class ThemeColorPreview {
    private final GTheme theme;
    private final BufferedImage image = new BufferedImage(1100, 780, BufferedImage.TYPE_INT_RGB);
    private final Graphics2D g = image.createGraphics();
    private final Font ui = new Font(Font.SANS_SERIF, Font.PLAIN, 14);
    private final Font code;

    private ThemeColorPreview(GTheme theme) {
        this.theme = theme;
        code = theme.getResolvedFont("font.decompiler").deriveFont(15f);
        g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING,
                           RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
    }

    private void box(String key, int x, int y, int width, int height) {
        g.setColor(java.util.Objects.requireNonNull(theme.getResolvedColor(key), key));
        g.fillRect(x, y, width, height);
    }

    private int text(String key, String value, int x, int y, Font font) {
        g.setColor(java.util.Objects.requireNonNull(theme.getResolvedColor(key), key));
        g.setFont(font);
        g.drawString(value, x, y);
        return x + g.getFontMetrics().stringWidth(value);
    }

    private void label(String value, int x, int y) {
        text("color.palette.vscode.fg.muted", value, x, y, ui);
    }

    private void listingLine(int y) {
        int x = text("color.fg.listing.address", "00401000  ", 42, y, code);
        x = text("color.fg.listing.mnemonic", "MOV  ", x, y, code);
        x = text("color.fg.listing.register", "RAX", x, y, code);
        x = text("color.fg.listing.separator", ", [RBP - ", x, y, code);
        x = text("color.fg.listing.constant", "0x8", x, y, code);
        text("color.fg.listing.separator", "]", x, y, code);
    }

    private void decompilerLine(int y) {
        int x = text("color.palette.vscode.keyword", "return ", 575, y, code);
        x = text("color.fg.decompiler.external.function", "decode", x, y, code);
        x = text("color.fg.decompiler", "(", x, y, code);
        x = text("color.fg.decompiler.variable", "buffer", x, y, code);
        text("color.fg.decompiler", ");", x, y, code);
    }

    private void draw(Path output) throws Exception {
        box("color.palette.vscode.chrome", 0, 0, 1100, 780);
        text("color.fg", "VS Code Dark Modern / Ghidra", 28, 34, ui.deriveFont(Font.BOLD, 20f));
        label("Theme color samples - rendered from Ghidra-resolved colors", 28, 60);
        String[] palette = {"editor", "chrome", "input", "border.subtle", "accent", "fg"};
        for (int i = 0; i < palette.length; i++) {
            String key = "color.palette.vscode." + palette[i];
            int x = 28 + i * 178;
            box(key, x, 88, 152, 18);
            Color c = theme.getResolvedColor(key);
            label(palette[i] + " " + String.format("#%02X%02X%02X", c.getRed(), c.getGreen(), c.getBlue()), x, 129);
        }

        box("color.bg.listing", 28, 158, 512, 222);
        box("color.bg.header.active", 28, 158, 512, 34);
        text("color.fg.header.active", "Listing - focused", 42, 181, ui);
        box("color.palette.vscode.accent", 28, 158, 512, 2);
        listingLine(222);
        box("color.bg.selection.listing", 38, 235, 490, 28);
        listingLine(255);
        box("color.bg.find.highlight.active", 38, 274, 490, 28);
        text("color.fg.listing.comment.eol", "; active search: decoded string", 42, 294, code);
        box("color.bg.find.highlight", 38, 312, 490, 28);
        text("color.fg.listing.comment.eol", "; another match", 42, 332, code);
        label("Syntax colors stay visible in selections and matches", 42, 367);

        box("color.bg.decompiler", 560, 158, 512, 222);
        box("color.bg.header.inactive", 560, 158, 512, 34);
        text("color.fg.header.inactive", "Decompiler", 575, 181, ui);
        decompilerLine(222);
        box("color.bg.selection", 570, 235, 490, 28);
        decompilerLine(255);
        box("color.bg.decompiler.highlights.find.active", 570, 274, 490, 28);
        text("color.fg.decompiler.comment", "// active search: buffer", 575, 294, code);
        box("color.bg.decompiler.current.variable", 570, 312, 490, 28);
        decompilerLine(332);
        label("Blue selection / amber search / neutral variable highlight", 575, 367);

        label("Debugger and byte edits", 28, 422);
        box("color.bg.table.row", 28, 437, 512, 40);
        text("color.fg.byteviewer.changed", "90 90   changed bytes", 42, 462, code);
        box("color.palette.vscode.list.selection", 28, 477, 512, 40);
        text("color.fg.debugger.value.changed.selected", "RAX     0x0000000000401000", 42, 502, code);
        box("color.palette.vscode.input", 28, 517, 512, 40);
        text("color.fg.error", "Invalid address", 42, 542, code);
        label("Bit-field cells", 560, 422);
        String[] cells = {"bit.active", "bit.component", "non.bit", "bit.conflict"};
        String[] names = {"editing", "flags", "value", "conflict"};
        for (int i = 0; i < cells.length; i++) {
            int x = 560 + i * 128;
            box("color.bg.plugin.editors.compositeeditor." + cells[i], x, 437, 124, 80);
            text("color.bg.plugin.editors.compositeeditor.text", names[i], x + 18, 482, code);
        }
        label("Light labels on dark, distinct cell backgrounds", 560, 542);

        label("Function Graph flow", 28, 604);
        String[] flows = {"fall.through", "jump.conditional", "jump.unconditional"};
        String[] flowLabels = {"Fall-through", "Conditional jump", "Unconditional jump"};
        for (int i = 0; i < flows.length; i++) {
            int x = 28 + i * 280;
            String key = "color.bg.plugin.functiongraph.edge." + flows[i];
            box(key, x, 630, 185, 3);
            text("color.fg.plugin.functiongraph.label.non.picked", flowLabels[i], x, 664, ui);
        }
        box("color.bg.plugin.functiongraph.edge.fall.through.highlight", 868, 630, 185, 3);
        text("color.fg.plugin.functiongraph.label.picked", "Highlighted path", 868, 664, ui);
        label("Standard editor, chrome, input, accent and syntax hues follow VS Code Dark Modern.", 28, 725);
        label("Selection/search fills and status text are adapted for Ghidra's renderers.", 28, 749);
        g.dispose();
        ImageIO.write(image, "png", output.toFile());
    }

    public static void render(GTheme theme, Path output) throws Exception {
        new ThemeColorPreview(theme).draw(output);
    }
}
