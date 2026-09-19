import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.nio.file.*;
import java.util.*;
import javax.imageio.ImageIO;
import javax.swing.Icon;

import generic.jar.ResourceFile;
import generic.theme.*;
import ghidra.framework.*;
import utility.application.ApplicationLayout;
import resources.MultiIcon;

/** Uses Ghidra's real ZIP reader and icon renderer, with isolated settings. */
public class GhidraThemeCheck {
    private static class TestLayout extends ApplicationLayout {
        TestLayout(Path install, Path settings) throws Exception {
            applicationInstallationDir = new ResourceFile(install.toFile());
            applicationRootDirs = List.of(new ResourceFile(install.resolve("Ghidra").toFile()));
            applicationProperties = new ApplicationProperties(applicationRootDirs);
            userSettingsDir = Files.createDirectories(settings).toFile();
            userTempDir = Files.createDirectories(settings.resolve("tmp")).toFile();
            userCacheDir = Files.createDirectories(settings.resolve("cache")).toFile();
            modules = Map.of();
            extensionInstallationDirs = List.of();
        }
    }

    private static void require(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }

    private static BufferedImage render(Icon icon, int width, int height) {
        require(icon != null, "Missing icon");
        BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = image.createGraphics();
        icon.paintIcon(null, g, 0, 0);
        g.dispose();
        return image;
    }

    private static String pixels(BufferedImage image) {
        return Arrays.toString(image.getRGB(0, 0, image.getWidth(), image.getHeight(),
                                           null, 0, image.getWidth()));
    }

    private static void checkSemanticIcons(GTheme theme, Path output) throws Exception {
        String[][] groups = {
            {"Functions", "icon.plugin.symboltree.node.", "function", "function.external", "function.thunk"},
            {"Data types", "icon.plugin.datatypes.", "structure", "union", "pointer"},
            {"Breakpoints", "icon.debugger.breakpoint.marker.", "enabled", "disabled", "mixed",
                "ineffective.enabled", "ineffective.disabled", "ineffective.mixed"},
            {"Graph paths", "icon.plugin.functiongraph.action.viewer.vertex.hover.",
                "paths.to.vertex", "paths.from.vertex", "paths.from.to.vertex", "paths.all"},
            {"Graph flow", "icon.plugin.functiongraph.action.viewer.vertex.hover.",
                "cycles", "cycles.all", "scoped.flow.forward", "scoped.flow.reverse"},
            {"Decompiler", "icon.decompiler.action.", "provider", "provider.readonly", "provider.unreachable"},
            {"Folders", "icon.plugin.datatypes.util.", "closed.folder", "closed.folder.locked",
                "open.folder", "open.folder.locked"},
            {"Type filters", "icon.plugin.datatypes.filter.", "arrays.off", "arrays.on", "pointers.off", "pointers.on"},
        };
        BufferedImage preview = new BufferedImage(1100, 950, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = preview.createGraphics();
        g.setColor(new java.awt.Color(0x1f1f1f));
        g.fillRect(0, 0, preview.getWidth(), preview.getHeight());
        g.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 12));
        g.setColor(new java.awt.Color(0xcccccc));
        g.drawString("VS Code Dark Modern / Ghidra icons - 16px actual size + 3x pixel preview", 20, 25);
        for (int row = 0; row < groups.length; row++) {
            String[] group = groups[row];
            Set<String> shapes = new HashSet<>();
            int y = 50 + row * 95;
            g.drawString(group[0], 20, y + 24);
            for (int col = 2; col < group.length; col++) {
                String key = group[1] + group[col];
                Icon icon = theme.getResolvedIcon(key);
                require(icon.getIconWidth() == 16 && icon.getIconHeight() == 16, "Wrong size: " + key);
                BufferedImage rendered = render(icon, 16, 16);
                int[] alpha = Arrays.stream(rendered.getRGB(0, 0, 16, 16, null, 0, 16))
                                    .map(p -> p >>> 24).toArray();
                require(Arrays.stream(alpha).sum() >= 8 * 255, "Empty or incomplete glyph: " + key);
                // Distinguish by shape even when hue cannot be perceived.
                require(shapes.add(Arrays.toString(alpha)), "Duplicate shape: " + key);
                int x = 155 + (col - 2) * 155;
                g.drawImage(rendered, x, y + 16, null);
                g.setRenderingHint(java.awt.RenderingHints.KEY_INTERPOLATION,
                                   java.awt.RenderingHints.VALUE_INTERPOLATION_NEAREST_NEIGHBOR);
                g.drawImage(rendered, x + 32, y, 48, 48, null);
                String label = group[col].replace("ineffective.", "ineff. ")
                    .replace("scoped.flow.", "scoped ").replace("paths.", "")
                    .replace("provider.", "").replace("function.", "");
                g.drawString(label, x, y + 68);
            }
        }
        Icon overlay = theme.getResolvedIcon("icon.debugger.breakpoint.overlay.inconsistent");
        BufferedImage overlayImage = render(overlay, 16, 16);
        require(Arrays.stream(overlayImage.getRGB(0, 0, 16, 16, null, 0, 16))
            .anyMatch(p -> (p >>> 24) != 0), "Empty inconsistency overlay");
        int x = 155;
        for (String state : List.of("enabled", "disabled", "mixed")) {
            Icon base = theme.getResolvedIcon("icon.debugger.breakpoint.marker." + state);
            BufferedImage before = render(base, 16, 16);
            BufferedImage after = render(new MultiIcon(base, overlay), 16, 16);
            require(!pixels(before).equals(pixels(after)), "Missing overlay: " + state);
            for (int y = 0; y < 16; y++) {
                for (int col = 0; col < 16; col++) {
                    if ((before.getRGB(col, y) >>> 24) != 0) {
                        require(before.getRGB(col, y) == after.getRGB(col, y),
                                "Overlay obscures breakpoint: " + state);
                    }
                }
            }
            g.drawImage(after, x, 832, null);
            g.drawImage(after, x + 32, 816, 48, 48, null);
            g.drawString(state, x, 884);
            x += 155;
        }
        g.drawString("Inconsistent", 20, 840);
        g.drawString("Application", 20, 925);
        for (int size : List.of(16, 24)) {
            BufferedImage app = render(theme.getResolvedIcon("icon.base.application." + size), size, size);
            long white = Arrays.stream(app.getRGB(0, 0, size, size, null, 0, size))
                .filter(p -> ((p >> 16) & 255) > 200 && ((p >> 8) & 255) > 200 && (p & 255) > 200).count();
            require(white > 10, "Application icon has lost its white circuit: " + size);
            g.drawImage(app, 155 + (size - 16) * 12, 907, null);
        }
        g.dispose();
        ImageIO.write(preview, "png", output.toFile());
    }

    public static void main(String[] args) throws Exception {
        Path install = Path.of(args[0]);
        Path settings = Path.of(args[2]);
        ApplicationConfiguration config = new ApplicationConfiguration();
        config.setInitializeLogging(false);
        Application.initializeApplication(new TestLayout(install, settings), config);
        GTheme theme = GTheme.loadTheme(new File(args[1]));
        require(theme != null, "Theme was not loaded");
        require(theme.getIcons().size() == 866, "Some icon definitions failed to parse");
        for (ColorValue color : theme.getColors()) {
            require(color.hasResolvableValue(theme), "Unresolved color: " + color.getId());
        }
        for (FontValue font : theme.getFonts()) {
            require(font.hasResolvableValue(theme), "Unresolved font: " + font.getId());
        }
        for (IconValue icon : theme.getIcons()) {
            require(icon.hasResolvableValue(theme), "Unresolved icon: " + icon.getId());
        }

        BufferedImage preview = new BufferedImage(320, 100, BufferedImage.TYPE_INT_ARGB);
        Graphics2D graphics = preview.createGraphics();
        graphics.setColor(new java.awt.Color(0x1f1f1f));
        graphics.fillRect(0, 0, 320, 100);
        Set<String> states = new HashSet<>();
        String prefix = "icon.version.tracking.match.table.markup.status.";
        String[] names = {"not.applied", "applied", "rejected", "ignored", "error"};
        for (int i = 0; i < names.length; i++) {
            BufferedImage image = render(theme.getResolvedIcon(prefix + names[i]), 45, 16);
            int painted = 0;
            for (int y = 0; y < 16; y++) {
                for (int x = 0; x < 45; x++) {
                    if ((image.getRGB(x, y) >>> 24) != 0) {
                        painted++;
                        require(x >= i * 9 && x < i * 9 + 8 && y >= 4 && y < 12,
                                "Status icon escapes its cell: " + names[i]);
                    }
                }
            }
            require(painted > 0, "Invisible status: " + names[i]);
            states.add(pixels(image.getSubimage(i * 9, 4, 8, 8)));
            graphics.drawImage(image, 8, 4, null);
        }
        require(states.size() == names.length, "Status glyphs are identical");
        Icon disabled = theme.getResolvedIcon(prefix + "disabled");
        require(disabled.getIconWidth() == 8 && disabled.getIconHeight() == 8,
                "Disabled cell has the wrong size");
        require(!pixels(render(disabled, 8, 8)).equals(pixels(render(
            theme.getResolvedIcon(prefix + "ignored"), 45, 16).getSubimage(27, 4, 8, 8))),
            "Ignored status looks disabled");

        for (String framePrefix : List.of("icon.task.progress", "icon.task.progress.hourglass")) {
            int count = framePrefix.endsWith("hourglass") ? 11 : 7;
            int size = count == 11 ? 24 : 16;
            Set<String> frames = new HashSet<>();
            for (int i = 1; i <= count; i++) {
                Icon icon = theme.getResolvedIcon(framePrefix + "." + i);
                require(icon.getIconWidth() == size && icon.getIconHeight() == size,
                        "Animation frame size changes");
                BufferedImage frame = render(icon, size, size);
                frames.add(pixels(frame));
                graphics.drawImage(frame, 8 + (i - 1) * 28, count == 11 ? 64 : 36, null);
            }
            require(frames.size() == count, "Progress animation contains identical frames");
        }
        require(!pixels(render(theme.getResolvedIcon("icon.widget.filterpanel.filter.off"), 16, 16))
                    .equals(pixels(render(theme.getResolvedIcon("icon.widget.filterpanel.filter.on"), 16, 16))),
                "Filter states render identically");
        Icon close = theme.getResolvedIcon("icon.widget.tabs.close");
        Icon closeHover = theme.getResolvedIcon("icon.widget.tabs.close.highlight");
        require(closeHover.getIconWidth() == close.getIconWidth() &&
                closeHover.getIconHeight() == close.getIconHeight(), "Close hover changes tab geometry");
        require(!pixels(render(close, 16, 16)).equals(pixels(render(closeHover, 16, 16))),
                "Close button hover is invisible");
        graphics.drawImage(render(theme.getResolvedIcon("icon.widget.filterpanel.filter.off"), 16, 16), 80, 4, null);
        graphics.drawImage(render(theme.getResolvedIcon("icon.widget.filterpanel.filter.on"), 16, 16), 108, 4, null);
        Font editor = theme.getResolvedFont("font.decompiler");
        require(Font.MONOSPACED.equalsIgnoreCase(editor.getFamily()), "Editor is not a logical monospace font");
        require(graphics.getFontMetrics(editor).charWidth('i') == graphics.getFontMetrics(editor).charWidth('W'),
                "Editor character widths differ");
        graphics.dispose();
        ImageIO.write(preview, "png", new File(args[3]));
        checkSemanticIcons(theme, Path.of(args[3]).resolveSibling("icons-check.png"));
        ThemeColorPreview.render(theme, Path.of(args[3]).resolveSibling("colors-check.png"));
        javax.swing.SwingUtilities.invokeAndWait(() -> {
            try {
                WindowChromePreview.render(theme, Path.of(args[3]).resolveSibling("windows-check.png"));
            }
            catch (Exception e) { throw new RuntimeException(e); }
        });
        System.out.println("PASS: Ghidra " + Application.getApplicationVersion() +
                           " ZIP import, 866 icons, distinct semantic shapes, non-obscuring breakpoint overlays, " +
                           "status geometry, distinct animation frames, filters and monospace font");
    }
}
